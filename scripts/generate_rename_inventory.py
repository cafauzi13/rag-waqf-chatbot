"""
scripts/generate_rename_inventory.py

Tahap 4 (sebelum Kiriman B) -- generate DRAFT usulan penamaan ulang untuk
seluruh PDF di data/raw/{wakaf,zakat}/{regulasi,literasi}/, ditulis ke
results/inventaris_draft.xlsx untuk direview & dipoles manual.

ATURAN KERAS: script ini HANYA MEMBACA data/raw/ dan file cleaning_debug
yang sudah ada. TIDAK PERNAH me-rename, memindahkan, atau menghapus file
apa pun -- satu-satunya tulisan adalah file inventaris_draft.xlsx.

Format nama baru yang diusulkan: {DOMAIN}-{JENIS}-{NN}_{Judul-Singkat}.pdf
  DOMAIN dan JENIS diambil dari nama folder (wakaf/zakat, regulasi/literasi).
  NN adalah nomor urut 2 digit per grup (domain+jenis), diurutkan tahun
  (lama->baru) lalu abjad; dokumen tanpa tahun diletakkan di akhir grup.
  Judul-Singkat untuk regulasi diekstrak dengan regex (jenis peraturan +
  nomor + tahun) dari nama file, fallback ke teks halaman pertama hasil
  cleaning Tahap 1-3 kalau ada. Untuk literasi, dari judul yang sudah
  relatif bersih di nama file asli (setelah boilerplate scrape dibuang),
  fallback ke metadata PDF, fallback ke halaman pertama.

Baris dengan keyakinan "rendah" (regex gagal, tahun tak ketemu, judul
terpotong aneh, atau nama_baru_usulan duplikat) diwarnai kuning di xlsx
supaya gampang direview.
"""

import re
import sys
import unicodedata
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import RAW_DATA_DIR, RESULTS_DIR

OUTPUT_PATH = RESULTS_DIR / "inventaris_draft.xlsx"
CLEANING_DEBUG_DIR = RESULTS_DIR / "cleaning_debug"

DOMAIN_MAP = {"wakaf": "WKF", "zakat-infak-sedekah": "ZKT", "kurban": "KRB"}

# --- Koreksi & atribusi manual dari review penulis ---
# Regulasi yang nama filenya sendiri tidak menyebut nomor/tahun (regex
# gagal total), tapi penulis sudah tahu identitas resminya.
REGULASI_MANUAL_OVERRIDES = {
    "Fatwa-MUI-tentang-Wakaf-Uang.pdf": {"jenis_singkat": "FatwaMUI", "nomor": "2", "tahun": "2002"},
}

# Literasi yang judul/instansi penerbitnya perlu dikoreksi manual (nama file
# aslinya menyesatkan atau tidak menyebut instansi sama sekali).
LITERASI_MANUAL_OVERRIDES = {
    "067b5-panduan_wakaf.pdf": {"judul_lengkap": "Panduan Wakaf", "institusi": "Kemenag", "tahun": "2013"},
    "Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf": {"judul_lengkap": "Definisi Wakaf Uang", "institusi": "BWI", "tahun": ""},
}

# Instansi default per kategori untuk literasi yang tidak di-override manual
# di atas -- dokumen wakaf/literasi seluruhnya hasil scrape situs BWI,
# zakat/literasi seluruhnya terbitan BAZNAS (lihat halaman penerbit di
# masing-masing dokumen). Diminta penulis: penamaan literasi harus selalu
# menyebut instansi yang menerbitkan. Kurban sengaja TIDAK dapat default --
# baru ada 1 dokumen literasi ("... - PWNU Kediri.pdf") dan nama filenya
# sendiri sudah menyebut instansi penerbit apa adanya, jadi tidak perlu
# dipaksa tambah instansi generik.
LITERASI_DEFAULT_INSTITUTION = {"wakaf": "BWI", "zakat-infak-sedekah": "BAZNAS"}
JENIS_MAP = {"regulasi": "REG", "literasi": "LIT"}

YEAR_RE = r"(?:19|20)\d{2}"

# File yang sudah pernah di-rename ke format final (dari sesi generate+apply
# sebelumnya) HARUS dilewati dari re-derivasi -- kalau tidak, judul yang
# sudah bersih ikut ter-slugify lagi sebagai "judul" (mis. "WKF-LIT-01_..."
# dianggap bagian dari judul), menghasilkan prefix ganda yang rusak.
ALREADY_RENAMED_RE = re.compile(r"^([A-Z]{2,4})-(REG|LIT)-(\d{2})_(.+)\.pdf$")

# Pola jenis peraturan (dicoba berurutan, yang paling spesifik lebih dulu).
# Masing-masing dicari di string yang sudah dinormalisasi (huruf kecil,
# dash/underscore -> spasi, spasi berlebih dirapikan).
REGULASI_KEYWORD_PATTERNS = [
    ("UU", r"undang[\s]?undang(?:\s*ri)?|\buu\b"),
    ("PP", r"peraturan\s*pemerintah(?:\s*ri)?|\bpp\b"),
    ("Perpres", r"peraturan\s*presiden|\bperpres\b"),
    ("PBWI", r"peraturan\s*(?:ketua\s*badan\s*pelaksana\s*)?bwi|\bpbwi\b"),
    ("Permenag", r"peraturan\s*(?:menteri\s*agama|kemenag)|\bpma\b|\bpermenag\b"),
    ("Permentan", r"peraturan\s*menteri\s*pertanian|\bpermentan\b"),
    ("Perbaznas", r"peraturan\s*baznas|\bperbaznas\b"),
    ("FatwaMUI", r"fatwa\s*mui"),
    ("Kepdirjen", r"keputusan\s*direktur\s*jenderal|\bkepdirjen\b"),
    ("SE", r"surat\s*edaran\b"),
    # "Permen" generik (jenis kementerian tidak spesifik di luar yang sudah
    # dipetakan di atas). \bpermen\b tidak akan salah kena di dalam
    # "permentan" karena \b mensyaratkan batas kata tepat setelah "permen".
    ("Permen", r"\bpermen\b"),
    ("BAZNAS", r"\bbaznas\b"),
    ("MUI", r"\bmui\b"),
]

# Setelah kata kunci jenis ditemukan, cari nomor + tahun di jendela teks
# setelahnya. Dicoba 2 pola berurutan: (1) eksplisit didahului "No./Nomor"
# -- ini yang paling umum di dokumen resmi, boleh ada kata sisipan seperti
# "Republik Indonesia" di antara jenis dan "Nomor" karena pakai re.search
# (bukan match di posisi 0); (2) fallback tanpa kata "No./Nomor" sama
# sekali untuk nama file kompak seperti "PBWI-1-2020". "Tahun"/"Thn" di
# antara nomor & tahun bersifat opsional karena beberapa nama file langsung
# menaruh tahun setelah nomor.
NOMOR_TAHUN_PATTERNS = [
    # "nomor" dicoba SEBELUM "no\.?" -- alternasi regex berhenti di pilihan
    # pertama yang cocok, dan "no" adalah prefix dari "nomor", jadi kalau
    # "no\.?" dicoba duluan ia akan berhenti setelah "no" saja (tanpa
    # menyantap "mor"), menyisakan "mor" ikut masuk ke grup nomor.
    re.compile(r"(?:nomor|no\.?)\s*(?P<nomor>[\w. ]+?)\s*(?:tahun|thn)?\s*(?P<tahun>" + YEAR_RE + r")\b"),
    re.compile(r"(?P<nomor>\d[\w.]*)\s*(?:tahun|thn)?\s*(?P<tahun>" + YEAR_RE + r")\b"),
]

# Boilerplate yang menempel di nama file literasi hasil scrape situs BWI.
LITERASI_SUFFIX_RE = re.compile(
    r"\s*[-–]\s*Badan\s*Wakaf\s*Indonesia.*$", re.IGNORECASE
)
LEADING_HASH_OR_DATE_RE = re.compile(r"^(?:\d{8}|[0-9a-f]{4,10})-", re.IGNORECASE)


def normalize_for_regex(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[-_]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def slugify(text: str, max_len: int = 40) -> str:
    """ASCII, kata dipisah tanda hubung, dipotong di batas kata terdekat <= max_len."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^A-Za-z0-9]+", "-", ascii_text).strip("-")
    if len(ascii_text) <= max_len:
        return ascii_text
    truncated = ascii_text[:max_len]
    if "-" in truncated:
        truncated = truncated.rsplit("-", 1)[0]
    return truncated.strip("-")


def build_literasi_slug(title: str, institution: str, tahun: str, max_len: int = 40) -> str:
    """
    Slugify judul literasi TAPI cadangkan dulu ruang untuk instansi & tahun
    supaya keduanya tidak ikut terpotong kalau judulnya panjang (slugify()
    polos memotong dari kanan, yang akan menghilangkan instansi/tahun di
    ujung kalau judul aslinya sudah mepet 40 karakter).
    """
    suffix_parts = [p for p in [institution, tahun] if p]
    suffix = "-".join(slugify(p, 20) for p in suffix_parts)
    budget_for_title = max_len - len(suffix) - (1 if suffix else 0)
    title_slug = slugify(title, max(budget_for_title, 10))
    return "-".join(p for p in [title_slug, suffix] if p)


def extract_regulasi_from_text(text: str) -> Optional[Tuple[str, str, str]]:
    """
    Cari (jenis_singkat, nomor, tahun) di `text`. None kalau tidak ada kata
    kunci jenis peraturan sama sekali.

    PENTING: kalau beberapa jenis kata kunci sama-sama ketemu (mis. halaman
    pertama sebuah PP menyebut "PERATURAN PEMERINTAH ... NOMOR 25 TAHUN 2018"
    di judulnya sendiri, TAPI juga menyebut "UNDANG-UNDANG NOMOR 41 TAHUN
    2004" sebagai dasar hukum yang diacu) -- yang dipilih adalah kata kunci
    yang posisinya PALING AWAL di teks, bukan yang paling duluan dicoba di
    daftar pola. Preambul UU/dasar hukum yang diacu hampir selalu disebut
    SETELAH judul dokumen itu sendiri, jadi aturan "paling awal menang" ini
    cukup andal untuk kasus semacam itu.
    """
    normalized = normalize_for_regex(text)

    candidates = []
    for jenis_singkat, keyword_pattern in REGULASI_KEYWORD_PATTERNS:
        match = re.search(keyword_pattern, normalized)
        if match:
            candidates.append((match.start(), match.end(), jenis_singkat))
    if not candidates:
        return None

    candidates.sort(key=lambda c: c[0])
    _, keyword_end, jenis_singkat = candidates[0]

    window = normalized[keyword_end: keyword_end + 80]
    for pattern in NOMOR_TAHUN_PATTERNS:
        nt_match = pattern.search(window)
        if nt_match:
            return jenis_singkat, nt_match.group("nomor").strip(), nt_match.group("tahun").strip()

    # Kata kunci jenis ketemu tapi nomor/tahun tidak -- tetap kembalikan
    # jenisnya dengan nomor/tahun kosong, biar tetap ada draft judul (akan
    # ditandai keyakinan "rendah" oleh pemanggil karena nomor/tahun kosong).
    return jenis_singkat, "", ""


def get_cleaning_debug_first_page(kategori: str, jenis: str, stem: str) -> Optional[str]:
    """Ambil teks [Hal. 1] dari dump cleaning_debug kalau file-nya ada."""
    dump_path = CLEANING_DEBUG_DIR / f"{kategori}_{jenis}_{stem}.txt"
    if not dump_path.exists():
        return None
    content = dump_path.read_text(encoding="utf-8")
    match = re.search(r"\[Hal\. 1\]\s*(.*?)(?=\n\[Hal\. \d+\]|\Z)", content, re.DOTALL)
    return match.group(1).strip() if match else None


def get_pdf_metadata_title(pdf_path: Path) -> Optional[str]:
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            title = (pdf.metadata or {}).get("Title", "")
            return title.strip() if title and title.strip() else None
    except Exception:
        return None


def derive_regulasi_row(pdf_path: Path, kategori: str, jenis: str) -> dict:
    stem = pdf_path.stem

    if pdf_path.name in REGULASI_MANUAL_OVERRIDES:
        override = REGULASI_MANUAL_OVERRIDES[pdf_path.name]
        jenis_singkat, nomor, tahun = override["jenis_singkat"], override["nomor"], override["tahun"]
        return {
            "judul_singkat_usulan": slugify(f"{jenis_singkat}-{nomor}-{tahun}".strip("-"), 40),
            "sumber_ekstraksi": "manual",
            "keyakinan": "tinggi",
            "judul_lengkap": f"{jenis_singkat} Nomor {nomor} Tahun {tahun}",
            "tahun": tahun,
        }

    result = extract_regulasi_from_text(stem)
    sumber = "nama_file"
    if not result or not result[1] or not result[2]:
        first_page = get_cleaning_debug_first_page(kategori, jenis, stem)
        if first_page:
            fallback = extract_regulasi_from_text(first_page)
            if fallback and fallback[1] and fallback[2]:
                result = fallback
                sumber = "halaman_1"

    if not result:
        return {
            "judul_singkat_usulan": slugify(stem, 40) or "TIDAK-DIKETAHUI",
            "sumber_ekstraksi": "gagal",
            "keyakinan": "rendah",
            "judul_lengkap": "",
            "tahun": "",
        }

    jenis_singkat, nomor, tahun = result
    judul_singkat = slugify(f"{jenis_singkat}-{nomor}-{tahun}".strip("-"), 40)
    keyakinan = "tinggi" if (nomor and tahun) else "rendah"
    judul_lengkap = f"{jenis_singkat} Nomor {nomor} Tahun {tahun}".strip() if nomor or tahun else ""

    return {
        "judul_singkat_usulan": judul_singkat,
        "sumber_ekstraksi": sumber,
        "keyakinan": keyakinan,
        "judul_lengkap": judul_lengkap,
        "tahun": tahun,
    }


def derive_literasi_row(pdf_path: Path, kategori: str, jenis: str) -> dict:
    stem = pdf_path.stem

    # 0. Override manual (nama file menyesatkan atau instansi tak jelas dari filename).
    if pdf_path.name in LITERASI_MANUAL_OVERRIDES:
        override = LITERASI_MANUAL_OVERRIDES[pdf_path.name]
        judul_lengkap_penuh = " ".join(p for p in [override["judul_lengkap"], override["institusi"]] if p)
        return {
            "judul_singkat_usulan": build_literasi_slug(override["judul_lengkap"], override["institusi"], override["tahun"]),
            "sumber_ekstraksi": "manual",
            "keyakinan": "tinggi",
            "judul_lengkap": judul_lengkap_penuh,
            "tahun": override["tahun"],
        }

    # 1. Coba bersihkan nama file: buang boilerplate scrape BWI & prefix hash/tanggal.
    cleaned = LITERASI_SUFFIX_RE.sub("", stem)
    cleaned = LEADING_HASH_OR_DATE_RE.sub("", cleaned)
    cleaned = re.sub(r"[_]+", " ", cleaned).strip()

    judul_lengkap = ""
    sumber = ""
    keyakinan = "rendah"

    if len(cleaned) >= 8:
        judul_lengkap, sumber, keyakinan = cleaned, "nama_file", "tinggi"

    # 2. Fallback: metadata judul PDF.
    if not judul_lengkap:
        meta_title = get_pdf_metadata_title(pdf_path)
        if meta_title:
            judul_lengkap, sumber, keyakinan = meta_title, "metadata_pdf", "tinggi"

    # 3. Fallback: baris pertama teks halaman 1 hasil cleaning.
    if not judul_lengkap:
        first_page = get_cleaning_debug_first_page(kategori, jenis, stem)
        if first_page:
            first_line = first_page.strip().split("\n")[0]
            words = first_line.split()[:8]
            if words:
                judul_lengkap, sumber, keyakinan = " ".join(words), "halaman_1", "rendah"

    if not judul_lengkap:
        return {
            "judul_singkat_usulan": slugify(stem, 40) or "TIDAK-DIKETAHUI",
            "sumber_ekstraksi": "gagal",
            "keyakinan": "rendah",
            "judul_lengkap": "",
            "tahun": "",
        }

    tahun_match = re.search(YEAR_RE, judul_lengkap)
    tahun = tahun_match.group(0) if tahun_match else ""

    # Selalu sebutkan instansi penerbit di penamaan literasi (permintaan
    # penulis) -- default per kategori, dicadangkan ruangnya di slug supaya
    # tidak ikut terpotong kalau judul aslinya sudah panjang.
    institution = LITERASI_DEFAULT_INSTITUTION.get(kategori, "")
    judul_lengkap_penuh = judul_lengkap if not institution else f"{judul_lengkap} {institution}"

    return {
        "judul_singkat_usulan": build_literasi_slug(judul_lengkap, institution, tahun),
        "sumber_ekstraksi": sumber,
        "keyakinan": keyakinan,
        "judul_lengkap": judul_lengkap_penuh,
        "tahun": tahun,
    }


def build_rows() -> list:
    rows = []
    for kategori_dir in sorted(RAW_DATA_DIR.iterdir()):
        if not kategori_dir.is_dir() or kategori_dir.name not in DOMAIN_MAP:
            continue
        for jenis_dir in sorted(kategori_dir.iterdir()):
            if not jenis_dir.is_dir() or jenis_dir.name not in JENIS_MAP:
                continue
            kategori, jenis = kategori_dir.name, jenis_dir.name
            expected_domain = DOMAIN_MAP[kategori]
            expected_jenis_kode = JENIS_MAP[jenis]

            for pdf_path in sorted(jenis_dir.glob("*.pdf")):
                already = ALREADY_RENAMED_RE.match(pdf_path.name)
                if already and already.group(1) == expected_domain and already.group(2) == expected_jenis_kode:
                    # Sudah dalam format final (dari sesi rename sebelumnya) --
                    # dilewati apa adanya, TIDAK diproses ulang.
                    tahun_match = re.search(YEAR_RE, pdf_path.name)
                    rows.append({
                        "nama_lama": pdf_path.name,
                        "folder": f"{kategori}/{jenis}",
                        "domain": expected_domain,
                        "jenis_kode": expected_jenis_kode,
                        "id_usulan": already.group(3),
                        "judul_singkat_usulan": already.group(4),
                        "nama_baru_usulan": pdf_path.name,
                        "sumber_ekstraksi": "sudah_rapi",
                        "keyakinan": "tinggi",
                        "judul_lengkap": "",
                        "tahun": tahun_match.group(0) if tahun_match else "",
                    })
                    continue

                if jenis == "regulasi":
                    extracted = derive_regulasi_row(pdf_path, kategori, jenis)
                else:
                    extracted = derive_literasi_row(pdf_path, kategori, jenis)

                rows.append({
                    "nama_lama": pdf_path.name,
                    "folder": f"{kategori}/{jenis}",
                    "domain": expected_domain,
                    "jenis_kode": expected_jenis_kode,
                    **extracted,
                })
    return rows


def assign_ids_and_new_names(rows: list) -> None:
    """
    Urutkan tiap grup (domain+jenis) per tahun (lama->baru) lalu abjad,
    dokumen tanpa tahun ditaruh di akhir grup urut abjad, lalu isi id_usulan
    & nama_baru_usulan in-place -- HANYA untuk baris yang belum final
    (sumber_ekstraksi != "sudah_rapi"). Baris yang sudah final dilewati
    sama sekali, dan penomoran baris baru di satu grup melanjutkan dari
    NN tertinggi yang sudah dipakai baris final grup itu (bukan mulai dari
    01 lagi), supaya tidak tabrakan nomor saat menambah dokumen baru ke
    grup yang sudah pernah di-rename sebagian.
    """
    from collections import defaultdict

    groups = defaultdict(list)
    max_existing_nn = defaultdict(int)
    for row in rows:
        key = (row["domain"], row["jenis_kode"])
        if row.get("sumber_ekstraksi") == "sudah_rapi":
            max_existing_nn[key] = max(max_existing_nn[key], int(row["id_usulan"]))
        else:
            groups[key].append(row)

    for (domain, jenis_kode), group_rows in groups.items():
        def sort_key(r):
            has_year = bool(r["tahun"])
            year_val = int(r["tahun"]) if has_year else 0
            return (0 if has_year else 1, year_val, r["nama_lama"].lower())

        group_rows.sort(key=sort_key)
        start = max_existing_nn[(domain, jenis_kode)] + 1
        for offset, row in enumerate(group_rows):
            nn = f"{start + offset:02d}"
            row["id_usulan"] = nn
            row["nama_baru_usulan"] = f"{domain}-{jenis_kode}-{nn}_{row['judul_singkat_usulan']}.pdf"


def flag_duplicates(rows: list) -> list:
    from collections import Counter
    name_counts = Counter(r["nama_baru_usulan"] for r in rows)
    duplicates = [name for name, count in name_counts.items() if count > 1]
    for row in rows:
        if row["nama_baru_usulan"] in duplicates:
            row["keyakinan"] = "rendah"
    return duplicates


def write_xlsx(rows: list) -> None:
    columns = [
        "nama_lama", "folder", "id_usulan", "judul_singkat_usulan",
        "nama_baru_usulan", "sumber_ekstraksi", "keyakinan", "judul_lengkap",
        "tahun", "catatan_calon_pertanyaan",
    ]
    df = pd.DataFrame(rows)
    df["catatan_calon_pertanyaan"] = ""
    df = df[columns]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="inventaris")
        worksheet = writer.sheets["inventaris"]

        header_font = Font(bold=True)
        yellow_fill = PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid")

        for col_idx in range(1, len(columns) + 1):
            worksheet.cell(row=1, column=col_idx).font = header_font
            worksheet.column_dimensions[get_column_letter(col_idx)].width = 28

        keyakinan_col_idx = columns.index("keyakinan") + 1
        for row_idx, row in enumerate(rows, start=2):
            if row["keyakinan"] == "rendah":
                for col_idx in range(1, len(columns) + 1):
                    worksheet.cell(row=row_idx, column=col_idx).fill = yellow_fill

        worksheet.freeze_panes = "A2"

    print(f"[SUCCESS] Inventaris draft tersimpan di: {OUTPUT_PATH}")


def print_summary(rows: list, duplicates: list) -> None:
    from collections import Counter

    print("\n=== RINGKASAN ===")
    group_counts = Counter((r["folder"]) for r in rows)
    for folder, count in sorted(group_counts.items()):
        print(f"  {folder}: {count} file")

    keyakinan_counts = Counter(r["keyakinan"] for r in rows)
    print(f"\nKeyakinan tinggi: {keyakinan_counts.get('tinggi', 0)}")
    print(f"Keyakinan rendah: {keyakinan_counts.get('rendah', 0)}")

    if duplicates:
        print(f"\n[WARNING] {len(duplicates)} nama_baru_usulan duplikat:")
        for name in duplicates:
            print(f"  - {name}")
    else:
        print("\nTidak ada nama_baru_usulan yang duplikat.")


def main():
    print(f"[INFO] Memindai PDF di '{RAW_DATA_DIR}' (read-only, tidak ada file yang di-rename/dipindah/dihapus)...")
    rows = build_rows()
    print(f"[INFO] Ditemukan {len(rows)} file PDF.")

    assign_ids_and_new_names(rows)
    duplicates = flag_duplicates(rows)
    write_xlsx(rows)
    print_summary(rows, duplicates)


if __name__ == "__main__":
    main()
