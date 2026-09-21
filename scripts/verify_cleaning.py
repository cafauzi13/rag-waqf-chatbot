"""
scripts/verify_cleaning.py

Tahap 6 (Verifikasi Cleaning) -- jalankan ekstraksi + cleaning
(src/cleaning.py, via src.ingest.process_pdf_file) atas SELURUH PDF di
data/raw/, lalu:

  1. Dump teks bersih tiap dokumen ke file .txt di results/cleaning_debug/,
     supaya bisa dibaca manual per dokumen.
  2. Simpan ringkasan statistik per dokumen + agregat per kategori x jenis
     ke results/cleaning_debug/summary.csv.

Ini BUKAN evaluasi otomatis -- cleaning dianggap selesai hanya setelah
penulis membaca sampel dari kedua jenis dokumen (regulasi & literasi) di
kedua kategori (wakaf & zakat) dan menyatakan hasilnya layak.
"""

import sys
from pathlib import Path

import pandas as pd

# Konsol Windows default ke cp1252, yang tidak bisa menampilkan sebagian
# karakter baris header/footer (mis. simbol panah dari web BWI). Paksa UTF-8
# supaya print() tidak crash saat menampilkan contoh baris yang terdeteksi.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.ingest import process_pdf_file
from src.config import RAW_DATA_DIR, RESULTS_DIR

OUTPUT_DIR = RESULTS_DIR / "cleaning_debug"


def derive_kategori_jenis(pdf_path: Path, raw_dir: Path) -> tuple:
    """
    Ambil kategori (wakaf/zakat) & jenis (regulasi/literasi) dari posisi
    file relatif terhadap data/raw/<kategori>/<jenis>/... Dipakai di sini
    hanya untuk penamaan file dump -- bukan src/metadata.py penuh (itu
    bagian Kiriman B, dipakai untuk metadata chunk sungguhan).
    """
    try:
        rel_parts = pdf_path.relative_to(raw_dir).parts
        kategori = rel_parts[0] if len(rel_parts) > 0 else "unknown"
        jenis = rel_parts[1] if len(rel_parts) > 1 else "unknown"
    except ValueError:
        kategori, jenis = "unknown", "unknown"
    return kategori, jenis


def main():
    pdf_files = sorted(RAW_DATA_DIR.rglob("*.pdf"))
    if not pdf_files:
        print(f"[ERROR] Tidak ditemukan file PDF di '{RAW_DATA_DIR}'.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Ditemukan {len(pdf_files)} file PDF. Memulai verifikasi cleaning...")

    rows = []

    for i, pdf_path in enumerate(pdf_files, start=1):
        kategori, jenis = derive_kategori_jenis(pdf_path, RAW_DATA_DIR)
        print(f"[{i}/{len(pdf_files)}] ({kategori}/{jenis}) {pdf_path.name}")

        try:
            cleaned_pages, report = process_pdf_file(pdf_path)
        except Exception as e:
            print(f"    [ERROR] Gagal memproses: {e}")
            rows.append({
                "kategori": kategori,
                "jenis": jenis,
                "source": pdf_path.name,
                "total_halaman": None,
                "halaman_dibuang": None,
                "halaman_final": None,
                "baris_header_footer_terdeteksi": None,
                "panjang_teks_akhir": None,
                "error": str(e),
            })
            continue

        full_text = "\n\n".join(f"[Hal. {page_num}]\n{text}" for page_num, text in cleaned_pages)

        dump_filename = f"{kategori}_{jenis}_{pdf_path.stem}.txt"
        dump_path = OUTPUT_DIR / dump_filename
        with open(dump_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        rows.append({
            "kategori": kategori,
            "jenis": jenis,
            "source": pdf_path.name,
            "total_halaman": report.total_pages,
            "halaman_dibuang": len(report.dropped_pages),
            "halaman_final": report.final_pages,
            "baris_header_footer_terdeteksi": len(report.header_footer_lines),
            "panjang_teks_akhir": len(full_text),
            "error": "",
        })

        if report.dropped_pages:
            alasan = ", ".join(f"hal.{p}({r})" for p, r in report.dropped_pages)
            print(f"    - Halaman dibuang: {alasan}")
        if report.header_footer_lines:
            contoh = list(report.header_footer_lines)[:3]
            print(f"    - Contoh baris header/footer terdeteksi: {contoh}")

    df = pd.DataFrame(rows)
    summary_path = OUTPUT_DIR / "summary.csv"
    df.to_csv(summary_path, index=False, encoding="utf-8")

    print(f"\n[SUCCESS] Dump teks bersih tersimpan di: {OUTPUT_DIR}")
    print(f"[SUCCESS] Ringkasan statistik tersimpan di: {summary_path}")

    valid_df = df[df["error"] == ""]
    if not valid_df.empty:
        agg = valid_df.groupby(["kategori", "jenis"]).agg(
            jumlah_dokumen=("source", "count"),
            total_halaman=("total_halaman", "sum"),
            total_halaman_dibuang=("halaman_dibuang", "sum"),
            rata2_header_footer_per_dok=("baris_header_footer_terdeteksi", "mean"),
        )
        print("\n=== RINGKASAN AGREGAT PER KATEGORI x JENIS ===")
        print(agg.to_string())

    error_count = (df["error"] != "").sum()
    if error_count:
        print(f"\n[WARNING] {error_count} file gagal diproses -- lihat kolom 'error' di summary.csv.")


if __name__ == "__main__":
    main()
