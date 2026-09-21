"""
src/cleaning.py

Fungsi-fungsi cleaning teks hasil ekstraksi PDF, masing-masing murni
(input/output teks atau list halaman) sehingga bisa dites sendiri tanpa
perlu membuka file PDF sungguhan.

Dipakai oleh src/ingest.py (proses ingestion sungguhan) dan
scripts/verify_cleaning.py (dump hasil cleaning untuk diperiksa manual).
"""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

# Pola penanda struktur dokumen regulasi (BAB, Pasal, ayat, huruf, diktum
# fatwa), daftar bernomor angka (1. 2. 6.), dan daftar huruf kapital/kecil
# (A. a.). Dipakai di join_wrapped_lines() untuk menghindari penggabungan
# baris yang justru memulai unit struktur/daftar baru.
STRUCTURE_MARKER_RE = re.compile(
    r"^(BAB\s+[IVXLC]+\b|Pasal\s+\d+|\(\d+\)|\d+\.\s|[a-zA-Z]\.\s|(Pertama|Kedua|Ketiga|Keempat)\s*:)"
)

# Rentang Unicode blok Arab (Tahap 1.5 -- buang teks Arab, pertahankan
# terjemahannya) DAN Arabic Presentation Forms A/B (mis. simbol "ﷺ" di
# U+FDFA, ligatur lain di U+FB50-FDFF dan U+FE70-FEFF) yang berada di luar
# blok Arab standar sehingga perlu rentang terpisah.
ARABIC_RE = re.compile(r"[؀-ۿﭐ-﷿ﹰ-﻿]+")

# Baris yang isinya murni nomor halaman (opsional diapit tanda hubung/dash),
# misal "12", "- 12 -", "– 12 –". Nomor berbeda tiap halaman sehingga tidak
# akan pernah exact-match satu sama lain -- dinormalisasi ke token yang sama
# supaya tetap terdeteksi sebagai elemen berulang oleh detect_header_footer_lines().
PAGE_NUMBER_LINE_RE = re.compile(r"^[-–—]?\s*\d+\s*[-–—]?$")
_PAGE_NUMBER_TOKEN = "\0PAGE_NUMBER\0"


def _normalize_for_frequency(line: str) -> str:
    return _PAGE_NUMBER_TOKEN if PAGE_NUMBER_LINE_RE.match(line) else line


@dataclass
class CleaningReport:
    """Ringkasan proses cleaning satu dokumen, untuk verifikasi manual."""
    source: str
    total_pages: int
    dropped_pages: List[Tuple[int, str]] = field(default_factory=list)
    header_footer_lines: Set[str] = field(default_factory=set)
    final_pages: int = 0


def detect_header_footer_lines(
    pages: List[str],
    threshold: float,
    window_lines: int = 3,
    min_pages: int = 4,
) -> Set[str]:
    """
    Untuk tiap posisi relatif 0..window_lines-1 dihitung dari awal DAN dari
    akhir halaman, cek apakah teks baris yang SAMA PERSIS muncul di posisi
    itu pada lebih dari `threshold` proporsi halaman -- ini menangkap kop
    surat/footer multi-baris (mis. "PRESIDEN" / "REPUBLIK INDONESIA" / "- 2 -"
    masing-masing di posisi 0/1/2) tanpa ikut menghapus konten asli yang
    kebetulan senada di halaman berbeda tapi TIDAK di posisi yang konsisten.

    Deteksi dilewati (mengembalikan set kosong) untuk dokumen dengan kurang
    dari `min_pages` halaman -- dengan sampel sesedikit itu, kemunculan
    berulang tidak bisa dibedakan dari kebetulan (rawan false positive pada
    dokumen literasi pendek 1-3 halaman).

    Baris berbentuk nomor halaman murni dinormalisasi ke token yang sama
    sebelum dihitung, karena angkanya berbeda tiap halaman dan tidak akan
    pernah exact-match satu sama lain.
    """
    if len(pages) < min_pages:
        return set()

    n = len(pages)
    head_counts = [Counter() for _ in range(window_lines)]
    tail_counts = [Counter() for _ in range(window_lines)]

    for page in pages:
        lines = [l.strip() for l in page.splitlines() if l.strip()]
        if not lines:
            continue
        for i in range(min(window_lines, len(lines))):
            head_counts[i][_normalize_for_frequency(lines[i])] += 1
            tail_counts[i][_normalize_for_frequency(lines[-1 - i])] += 1

    result: Set[str] = set()
    for i in range(window_lines):
        for line, count in head_counts[i].items():
            if (count / n) > threshold:
                result.add(line)
        for line, count in tail_counts[i].items():
            if (count / n) > threshold:
                result.add(line)
    return result


def strip_header_footer(pages: List[str], header_footer_lines: Set[str]) -> List[str]:
    """
    Buang baris yang cocok dengan `header_footer_lines` dari tiap halaman.
    Jika token nomor halaman ada di `header_footer_lines`, seluruh baris
    berbentuk nomor halaman murni ikut dibuang (bukan cuma yang exact-match
    satu angka tertentu).
    """
    if not header_footer_lines:
        return list(pages)

    strip_page_numbers = _PAGE_NUMBER_TOKEN in header_footer_lines

    cleaned = []
    for page in pages:
        kept_lines = []
        for line in page.splitlines():
            stripped = line.strip()
            if stripped in header_footer_lines:
                continue
            if strip_page_numbers and PAGE_NUMBER_LINE_RE.match(stripped):
                continue
            kept_lines.append(line)
        cleaned.append("\n".join(kept_lines))
    return cleaned


def dehyphenate(text: str) -> str:
    """Gabungkan kata yang terputus tanda hubung di akhir baris: 'pengelo-\\nlaan' -> 'pengelolaan'."""
    return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)


def join_wrapped_lines(text: str) -> str:
    """
    Gabungkan baris berikutnya ke baris sekarang JIKA baris sekarang tidak
    diakhiri tanda baca akhir (. : ;) DAN baris berikutnya tidak diawali
    penanda struktur dokumen (BAB/Pasal/ayat/huruf/diktum). Baris kosong
    dipertahankan sebagai pemisah paragraf.
    """
    lines = text.split("\n")
    result: List[str] = []
    buffer = ""

    def flush():
        nonlocal buffer
        if buffer:
            result.append(buffer)
            buffer = ""

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            flush()
            result.append("")
            continue

        if not buffer:
            buffer = stripped
            continue

        prev_ends_terminal = buffer.rstrip().endswith((".", ":", ";"))
        next_is_structure_marker = bool(STRUCTURE_MARKER_RE.match(stripped))

        if not prev_ends_terminal and not next_is_structure_marker:
            buffer = buffer.rstrip() + " " + stripped
        else:
            flush()
            buffer = stripped

    flush()
    return "\n".join(result)


def strip_arabic_blocks(text: str) -> str:
    """Buang rentang Unicode Arab (termasuk Presentation Forms); sistem hanya melayani Bahasa Indonesia."""
    return ARABIC_RE.sub("", text)


def _is_pure_punctuation_token(token: str) -> bool:
    """Token dianggap 'murni tanda baca' jika tidak mengandung huruf/angka sama sekali."""
    return not re.search(r"\w", token, flags=re.UNICODE)


def strip_arabic_residue_punctuation(text: str) -> str:
    """
    Buang RUN (2 token atau lebih beruntun) tanda baca murni yang tersisa
    setelah blok Arab dibuang -- mis. footnote/harakat yang representasinya
    jadi pecahan seperti ": - : ." atau "( ) , , ,". Beroperasi per token
    yang dipisah spasi, per baris (supaya struktur baris tidak terganggu).
    Satu tanda baca berdiri sendiri (mis. tanda hubung di "kata - kata")
    tetap dipertahankan -- hanya run 2+ yang dibuang, karena run sepanjang
    itu hampir selalu sisa artefak, bukan tanda baca Indonesia yang sah.
    """
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        tokens = line.split(" ")
        result: List[str] = []
        buffer: List[str] = []
        for tok in tokens:
            if _is_pure_punctuation_token(tok):
                buffer.append(tok)
            else:
                if len(buffer) == 1:
                    result.append(buffer[0])
                buffer = []
                result.append(tok)
        if len(buffer) == 1:
            result.append(buffer[0])
        cleaned_lines.append(" ".join(result))
    return "\n".join(cleaned_lines)


def normalize_whitespace(text: str) -> str:
    """Rapikan spasi ganda, baris kosong berlebih, dan trim keseluruhan teks."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_non_substantive_page(
    text: str,
    min_page_chars: int,
    dot_leader_ratio_threshold: float,
    blank_underscore_ratio_threshold: float,
) -> Tuple[bool, Optional[str]]:
    """
    Deteksi halaman non-substantif:
      - lebih pendek dari `min_page_chars` (halaman kosong/nyaris kosong)
      - didominasi baris "leader dot" (daftar isi, mis. "..... 12")
      - didominasi baris kosong/underscore (formulir, lembar tanda tangan)
    Mengembalikan (True, alasan) jika halaman harus dibuang, else (False, None).
    """
    stripped = text.strip()
    if len(stripped) < min_page_chars:
        return True, "halaman_terlalu_pendek_atau_kosong"

    all_lines = stripped.split("\n")
    non_empty_lines = [l for l in all_lines if l.strip()]
    if not non_empty_lines:
        return True, "halaman_kosong"

    dot_leader_lines = sum(1 for l in non_empty_lines if re.search(r"\.{4,}", l))
    if (dot_leader_lines / len(non_empty_lines)) > dot_leader_ratio_threshold:
        return True, "daftar_isi_atau_leader_dot"

    # Sebagian dokumen memberi daftar isi tanpa leader-dot sama sekali --
    # nomor halaman dipisah pakai bullet/dash biasa (kadang glyph khusus di
    # Private Use Area font, bukan karakter Unicode standar). Dot-leader di
    # atas tidak menangkapnya, tapi judul "DAFTAR ISI" hampir selalu ditulis
    # verbatim sebagai baris pertama halaman itu.
    if re.match(r"^DAFTAR\s+ISI\b", non_empty_lines[0].strip(), re.IGNORECASE):
        return True, "daftar_isi_eksplisit"

    blank_or_underscore_lines = sum(
        1 for l in all_lines if not l.strip() or re.fullmatch(r"[_\-\s]{3,}", l.strip())
    )
    if (blank_or_underscore_lines / len(all_lines)) > blank_underscore_ratio_threshold:
        return True, "formulir_atau_lembar_kosong"

    return False, None


def clean_document(
    pages: List[str],
    header_footer_threshold: float,
    min_page_chars: int,
    dot_leader_ratio_threshold: float,
    blank_underscore_ratio_threshold: float,
    header_footer_window_lines: int = 3,
    min_pages_for_header_footer_detection: int = 4,
    source: str = "",
) -> Tuple[List[Tuple[int, str]], CleaningReport]:
    """
    Orkestrasi cleaning satu dokumen (list teks mentah per halaman, index-0
    = halaman 1). Urutan: buang halaman non-substantif -> deteksi & buang
    header/footer (dihitung dari halaman yang tersisa saja) -> per halaman:
    dehyphenate -> gabung baris terpotong -> buang blok Arab -> normalisasi
    whitespace.

    Mengembalikan list (nomor_halaman_asli, teks_bersih) -- nomor halaman
    asli dipertahankan supaya metadata `page` tetap benar walau ada halaman
    yang dibuang.
    """
    dropped_pages: List[Tuple[int, str]] = []
    kept_pages: List[str] = []
    kept_page_numbers: List[int] = []

    for i, page_text in enumerate(pages):
        page_num = i + 1
        is_bad, reason = is_non_substantive_page(
            page_text, min_page_chars, dot_leader_ratio_threshold, blank_underscore_ratio_threshold
        )
        if is_bad:
            dropped_pages.append((page_num, reason))
        else:
            kept_pages.append(page_text)
            kept_page_numbers.append(page_num)

    header_footer_lines = detect_header_footer_lines(
        kept_pages, header_footer_threshold, header_footer_window_lines, min_pages_for_header_footer_detection
    )
    stripped_pages = strip_header_footer(kept_pages, header_footer_lines)

    final_pages: List[Tuple[int, str]] = []
    for page_num, page_text in zip(kept_page_numbers, stripped_pages):
        text = dehyphenate(page_text)
        text = join_wrapped_lines(text)
        text = strip_arabic_blocks(text)
        text = strip_arabic_residue_punctuation(text)
        text = normalize_whitespace(text)
        final_pages.append((page_num, text))

    # Ganti token internal nomor halaman dengan label yang bisa dibaca manusia
    # sebelum disimpan ke laporan (dipakai untuk print/CSV di verify_cleaning.py).
    reportable_header_footer_lines = {
        "<nomor halaman berulang>" if line == _PAGE_NUMBER_TOKEN else line
        for line in header_footer_lines
    }

    report = CleaningReport(
        source=source,
        total_pages=len(pages),
        dropped_pages=dropped_pages,
        header_footer_lines=reportable_header_footer_lines,
        final_pages=len(final_pages),
    )
    return final_pages, report
