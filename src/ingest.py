import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.chunking import chunk_segments
from src.cleaning import CleaningReport, clean_document
from src.metadata import derive_metadata_from_path
from src.segmentation import segment_literasi, segment_regulasi
from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    HEADER_FOOTER_THRESHOLD,
    HEADER_FOOTER_WINDOW_LINES,
    MIN_PAGES_FOR_HEADER_FOOTER_DETECTION,
    MIN_PAGE_CHARS,
    DOT_LEADER_RATIO_THRESHOLD,
    BLANK_UNDERSCORE_RATIO_THRESHOLD,
)

CHUNKS_JSONL_PATH = PROCESSED_DATA_DIR / "chunks.jsonl"


def extract_pdf_pages(pdf_path: Path) -> List[str]:
    """
    Ekstraksi teks mentah per halaman menggunakan pdfplumber (layout-aware).
    Fallback ke PyMuPDF jika pdfplumber gagal mem-parse file tertentu.
    """
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            return [(page.extract_text() or "") for page in pdf.pages]
    except Exception as e:
        print(f"[WARNING] pdfplumber gagal untuk '{pdf_path.name}' ({e}). Mencoba fallback PyMuPDF...")
        try:
            import fitz
            doc = fitz.open(str(pdf_path))
            pages = [page.get_text() for page in doc]
            doc.close()
            return pages
        except Exception as e2:
            print(f"[ERROR] PyMuPDF juga gagal untuk '{pdf_path.name}': {e2}")
            raise


# --- Pengecualian manual per dokumen (BUKAN aturan cleaning umum) ---
# Tabel 6 di halaman 45-46 "ZKT-LIT-01_Kajian-Nisab-Zakat-BAZNAS-2026.pdf" (nama
# lama sebelum Tahap 4: "Kajian Nisab Zakat Pendapatan dan Jasa 2026.pdf")
# rusak parsing-nya (kolom & data tercampur jadi satu baris tanpa pemisah --
# lihat results/cleaning_debug/kajian_nisab_hal45.png dan hal46.png untuk
# tabel aslinya, dibaca manual oleh penulis). Keputusan penulis: JANGAN
# perbaiki parser tabel secara umum, JANGAN tulis ulang angkanya di sini --
# cukup buang baris mentahnya dari hasil cleaning, supaya tidak ada dua
# versi (yang benar di gambar, yang rusak di teks) yang bersaing saat
# retrieval. Prosa kesimpulan di sekitarnya (halaman 45 & 46) dipertahankan.
_KAJIAN_NISAB_SOURCE = "ZKT-LIT-01_Kajian-Nisab-Zakat-BAZNAS-2026.pdf"
_KAJIAN_NISAB_HAL45_GARBLED_LINE = (
    "Tabel 6. Usulan Penetapan Nisab Zakat Pendapatan dan Jasa Tahun 2026 Proyeksi Nisab Harga "
    "rata-rata selama periode haul tahun 2025 Pertahun Perbulan SK Ketua BAZNAS 2025 Rp85,685,972 "
    "Rp7,140,498 Antam Rp179,975,311 Rp14,997,943 (Rp.2,117,357/gram) 24 Karat Rp153,623,652 "
    "Rp12,801,971 Usulan Tahun Standar (Rp.1,807,337/gram) 2026 Emas* 22 Karat Rp140,821,680 "
    "Rp11,735,140 (Rp.1,656,726/gram)"
)
_KAJIAN_NISAB_HAL46_GARBLED_PREFIX = (
    "Proyeksi Nisab Harga rata-rata selama periode haul tahun 2025 Pertahun Perbulan 21 Karat "
    "Rp135,188,813 Rp11,265,734 (Rp.1,590,457/gram) 16 Karat Rp108,796,270 Rp9,066,356 "
    "(Rp.1,279,956/gram) 14 Karat Rp91,681,728 Rp7,640,144 (1,078,609/gram) Standar Perak "
    "Rp29,605,415 Rp2,467,118 Perak (Rp. 22,145/gram) Beras Premium Rp102,400,080 Rp8,533,340 "
    "(Rp 16,285/kg) Beras Medium Ziraah Rp91,440,096 Rp7,620,008 (Rp 14,542/kg) Gabah Kering "
    "Giling Rp62,688,000 Rp5,224,000 (Rp.8000/kg) Sumber: Diolah peneliti, 2026 "
)


def _strip_known_garbled_tables(pages: List[Tuple[int, str]], source: str) -> List[Tuple[int, str]]:
    if source != _KAJIAN_NISAB_SOURCE:
        return pages
    result = []
    for page_num, text in pages:
        if page_num == 45 and _KAJIAN_NISAB_HAL45_GARBLED_LINE in text:
            text = text.replace(_KAJIAN_NISAB_HAL45_GARBLED_LINE, "").strip()
        elif page_num == 46 and _KAJIAN_NISAB_HAL46_GARBLED_PREFIX in text:
            text = text.replace(_KAJIAN_NISAB_HAL46_GARBLED_PREFIX, "").strip()
        result.append((page_num, text))
    return result


def process_pdf_file(pdf_path: Path) -> Tuple[List[Tuple[int, str]], CleaningReport]:
    """
    Ekstraksi + cleaning satu file PDF. Mengembalikan list (nomor_halaman,
    teks_bersih) beserta CleaningReport-nya. Dipakai oleh
    load_and_preprocess_pdfs() maupun scripts/verify_cleaning.py, supaya
    logikanya tidak terduplikasi.
    """
    raw_pages = extract_pdf_pages(pdf_path)
    cleaned_pages, report = clean_document(
        raw_pages,
        header_footer_threshold=HEADER_FOOTER_THRESHOLD,
        min_page_chars=MIN_PAGE_CHARS,
        dot_leader_ratio_threshold=DOT_LEADER_RATIO_THRESHOLD,
        blank_underscore_ratio_threshold=BLANK_UNDERSCORE_RATIO_THRESHOLD,
        header_footer_window_lines=HEADER_FOOTER_WINDOW_LINES,
        min_pages_for_header_footer_detection=MIN_PAGES_FOR_HEADER_FOOTER_DETECTION,
        source=pdf_path.name,
    )
    cleaned_pages = _strip_known_garbled_tables(cleaned_pages, pdf_path.name)
    return cleaned_pages, report


def build_chunks(raw_dir: Path) -> List[Dict[str, Any]]:
    """
    Pipeline lengkap PDF -> chunk siap index: ekstraksi -> cleaning ->
    metadata dari path -> segmentasi (Pasal/diktum untuk regulasi, heading
    untuk literasi) -> chunking per-segmen. Tidak menyentuh embedding/FAISS
    sama sekali -- itu tanggung jawab src/build_index.py, supaya ganti
    model embedding tidak perlu re-ekstraksi PDF dari awal.
    """
    pdf_files = sorted(raw_dir.rglob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"Tidak ditemukan file PDF di folder '{raw_dir}'.")

    print(f"[INFO] Ditemukan {len(pdf_files)} file PDF di '{raw_dir}'. Memulai pemrosesan...")

    all_chunks: List[Dict[str, Any]] = []

    for pdf_path in pdf_files:
        print(f"  - Memproses: {pdf_path.name}")
        cleaned_pages, report = process_pdf_file(pdf_path)
        print(
            f"    -> {report.final_pages}/{report.total_pages} halaman dipertahankan, "
            f"{len(report.dropped_pages)} dibuang, {len(report.header_footer_lines)} baris header/footer terdeteksi."
        )

        if not cleaned_pages:
            print(f"    [WARNING] Tidak ada teks yang bisa diekstrak dari '{pdf_path.name}' -- dilewati "
                  f"(kemungkinan PDF hasil scan tanpa lapisan teks; lihat README/laporan untuk daftarnya).")
            continue

        path_meta = derive_metadata_from_path(pdf_path, raw_dir)

        if path_meta["jenis"] == "regulasi":
            segments = segment_regulasi(cleaned_pages)
        else:
            segments = segment_literasi(cleaned_pages)

        doc_chunks = chunk_segments(
            segments,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            base_metadata=path_meta,
        )
        print(f"    -> {len(segments)} segmen -> {len(doc_chunks)} chunk.")
        all_chunks.extend(doc_chunks)

    print(f"[SUCCESS] Total {len(all_chunks)} chunk dari {len(pdf_files)} PDF.")
    return all_chunks


def write_chunks_jsonl(chunks: List[Dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"[SUCCESS] {len(chunks)} chunk ditulis ke '{output_path}'.")


def main():
    print("=== TAHAP 1: PDF -> chunks.jsonl ===")
    chunks = build_chunks(RAW_DATA_DIR)
    write_chunks_jsonl(chunks, CHUNKS_JSONL_PATH)
    print("=== SELESAI. Jalankan `python -m src.build_index` untuk membangun indeks FAISS. ===")


if __name__ == "__main__":
    main()
