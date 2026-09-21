"""
src/segmentation.py

Pecah teks hasil cleaning (src/cleaning.py) menjadi segmen berdasarkan
penanda struktur, SEBELUM chunking -- supaya satu unit argumen hukum
(satu Pasal, satu diktum fatwa, satu sub-bab) tidak terpotong di tengah
oleh chunking.

CATATAN DESAIN (menyimpang dari rencana awal, diinfokan ke penulis):
Rencana awal menyebut deteksi heading literasi berbasis ukuran font
(perlu metadata word-level dari pdfplumber). Setelah melihat isi
dokumen literasi yang sesungguhnya (mis. Kajian Nisab BAZNAS, Buku
Panduan ZIS), ternyata dokumen-dokumen itu SUDAH memakai penanda teks
eksplisit yang sama polanya dengan regulasi (mis. "A. PENDAHULUAN",
"BAB I PENDAHULUAN") -- bukan cuma dibedakan lewat ukuran font. Segmentasi
literasi di sini karena itu memakai pendekatan penanda-teks yang sama
seperti regulasi (lebih sederhana, tidak perlu ekstraksi font-size baru),
dengan fallback: dokumen literasi pendek yang sama sekali tidak punya
penanda (mayoritas artikel singkat BWI) jadi satu segmen utuh.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

PEMBUKAAN_UNIT = "Pembukaan"
DOKUMEN_UTUH_UNIT = "Dokumen Utuh"


@dataclass
class Segment:
    unit: str
    halaman_mulai: int
    halaman_akhir: int
    text: str


# Regulasi: Pasal & diktum fatwa sebagai batas segmen. BAB/Bagian sengaja
# TIDAK jadi batas sendiri (supaya tidak menghasilkan segmen nyaris kosong
# berisi cuma judul bab) -- baris BAB/Bagian ikut melebur ke segmen Pasal
# berikutnya yang didahuluinya.
_PASAL_RE = re.compile(r"^Pasal\s+(\d+)([A-Za-z]?)\b")
_DIKTUM_ORDER = [
    "Pertama", "Kedua", "Ketiga", "Keempat", "Kelima",
    "Keenam", "Ketujuh", "Kedelapan", "Kesembilan", "Kesepuluh",
]
_DIKTUM_RE = re.compile(r"^(" + "|".join(_DIKTUM_ORDER) + r")\s*:")
# (tidak ada REGULASI_MARKERS generik -- segment_regulasi() di bawah butuh
# state urutan menaik per tipe penanda, jadi ditulis manual, bukan lewat
# _segment_by_markers() generik yang dipakai segment_literasi())

# Literasi: heading huruf kapital ("A. PENDAHULUAN") atau BAB eksplisit.
_LITERASI_HEADING_RE = re.compile(r"^([A-Z])\.\s+[A-Z][A-Z\s]{2,}")
_LITERASI_BAB_RE = re.compile(r"^BAB\s+([IVXLC]+)\b")

_ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def _roman_to_int(roman: str) -> int:
    roman = roman.upper()
    total = 0
    prev = 0
    for ch in reversed(roman):
        value = _ROMAN_VALUES.get(ch, 0)
        total += value if value >= prev else -value
        prev = max(prev, value)
    return total


def _flatten_lines(pages: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """(halaman, teks_halaman) -> list (halaman, baris) untuk tiap baris non-kosong."""
    entries = []
    for page_num, text in pages:
        for line in text.split("\n"):
            if line.strip():
                entries.append((page_num, line))
    return entries


def segment_regulasi(pages: List[Tuple[int, str]]) -> List[Segment]:
    """
    Pecah per Pasal / diktum fatwa. Teks sebelum penanda pertama
    (Menimbang/Mengingat/dst) jadi segmen 'Pembukaan'.

    PENTING: nomor Pasal/diktum HARUS menaik dibanding yang terakhir
    diterima supaya dianggap batas segmen baru. Preambul "Menimbang" /
    "Mengingat" di hampir semua regulasi mengutip nomor Pasal dari
    undang-undang lain sebagai dasar hukum (mis. "untuk melaksanakan
    ketentuan Pasal 14, Pasal 21, Pasal 31...") -- tanpa aturan menaik ini,
    tiap kutipan itu salah dianggap Pasal baru dari dokumen ini sendiri,
    menghasilkan puluhan segmen palsu yang tidak berurutan. Konsekuensi:
    Pasal yang diubah lalu diulang penomorannya sendiri di dalam peraturan
    "Perubahan atas ..." (jarang terjadi) tidak akan terpecah jadi segmen
    baru -- teksnya melebur ke segmen sebelumnya, bukan hilang.
    """
    entries = _flatten_lines(pages)
    if not entries:
        return []

    segments: List[Segment] = []
    current_unit = PEMBUKAAN_UNIT
    current_lines: List[str] = []
    current_start_page = entries[0][0]
    last_page = entries[0][0]
    last_pasal_num = 0
    last_diktum_idx = -1
    seen_pasal_1 = False

    def flush(end_page: int):
        if current_lines:
            segments.append(Segment(
                unit=current_unit,
                halaman_mulai=current_start_page,
                halaman_akhir=end_page,
                text="\n".join(current_lines),
            ))

    for page_num, line in entries:
        stripped = line.strip()
        new_unit: Optional[str] = None

        m_pasal = _PASAL_RE.match(stripped)
        if m_pasal:
            num = int(m_pasal.group(1))
            if not seen_pasal_1:
                # Sebelum "Pasal 1" sungguhan ketemu, abaikan setiap "Pasal N"
                # -- hampir pasti kutipan dasar hukum yang terpotong baris di
                # klausa Menimbang/Mengingat (mis. "...ketentuan Pasal 13,\n
                # Pasal 14 ayat (2), Pasal 16..."), bukan Pasal dokumen ini.
                if num == 1:
                    seen_pasal_1 = True
                    new_unit = m_pasal.group(0).strip()
                    last_pasal_num = 1
            elif num > last_pasal_num:
                new_unit = m_pasal.group(0).strip()
                last_pasal_num = num

        if new_unit is None:
            m_diktum = _DIKTUM_RE.match(stripped)
            if m_diktum:
                idx = _DIKTUM_ORDER.index(m_diktum.group(1))
                if idx > last_diktum_idx:
                    new_unit = m_diktum.group(0).strip()
                    last_diktum_idx = idx

        if new_unit:
            flush(last_page)
            current_unit = new_unit
            current_lines = [line]
            current_start_page = page_num
        else:
            current_lines.append(line)
        last_page = page_num

    flush(last_page)

    if not segments:
        full_text = "\n".join(l for _, l in entries)
        return [Segment(
            unit=DOKUMEN_UTUH_UNIT,
            halaman_mulai=entries[0][0],
            halaman_akhir=entries[-1][0],
            text=full_text,
        )] if full_text.strip() else []

    return segments


def segment_literasi(pages: List[Tuple[int, str]]) -> List[Segment]:
    """
    Pecah per BAB (angka Romawi) atau heading huruf kapital ("A. JUDUL") kalau
    ada. Dokumen tanpa penanda jadi satu segmen 'Dokumen Utuh'.

    Pakai aturan menaik + gerbang "harus mulai dari BAB I / heading A" yang
    sama seperti segment_regulasi(), untuk kasus serupa (mis. badan teks
    menyebut "sebagaimana dijelaskan pada BAB II" sebagai rujukan silang).
    Catatan: ini TIDAK cukup untuk halaman Daftar Isi yang mencantumkan
    BAB I/II/III dalam urutan menaik yang sama seperti aslinya -- itu
    ditangani terpisah di src/cleaning.py (deteksi halaman "DAFTAR ISI"
    dibuang sebelum sampai ke segmentasi).
    """
    entries = _flatten_lines(pages)
    if not entries:
        return []

    segments: List[Segment] = []
    current_unit = PEMBUKAAN_UNIT
    current_lines: List[str] = []
    current_start_page = entries[0][0]
    last_page = entries[0][0]
    last_bab_num = 0
    seen_bab_1 = False
    last_heading_letter = ""
    seen_heading_a = False

    def flush(end_page: int):
        if current_lines:
            segments.append(Segment(
                unit=current_unit,
                halaman_mulai=current_start_page,
                halaman_akhir=end_page,
                text="\n".join(current_lines),
            ))

    for page_num, line in entries:
        stripped = line.strip()
        new_unit: Optional[str] = None

        m_bab = _LITERASI_BAB_RE.match(stripped)
        if m_bab:
            num = _roman_to_int(m_bab.group(1))
            if not seen_bab_1:
                if num == 1:
                    seen_bab_1 = True
                    new_unit = stripped[:80]
                    last_bab_num = 1
            elif num > last_bab_num:
                new_unit = stripped[:80]
                last_bab_num = num

        if new_unit is None:
            m_heading = _LITERASI_HEADING_RE.match(stripped)
            if m_heading:
                letter = m_heading.group(1)
                if not seen_heading_a:
                    if letter == "A":
                        seen_heading_a = True
                        new_unit = stripped[:80]
                        last_heading_letter = "A"
                elif letter > last_heading_letter:
                    new_unit = stripped[:80]
                    last_heading_letter = letter

        if new_unit:
            flush(last_page)
            current_unit = new_unit
            current_lines = [line]
            current_start_page = page_num
        else:
            current_lines.append(line)
        last_page = page_num

    flush(last_page)

    if not segments:
        full_text = "\n".join(l for _, l in entries)
        return [Segment(
            unit=DOKUMEN_UTUH_UNIT,
            halaman_mulai=entries[0][0],
            halaman_akhir=entries[-1][0],
            text=full_text,
        )] if full_text.strip() else []

    return segments
