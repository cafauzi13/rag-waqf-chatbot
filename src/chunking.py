"""
src/chunking.py

Chunking DI DALAM tiap segmen hasil src/segmentation.py -- tidak pernah
memotong lintas Pasal/heading. Setiap chunk akhir diberi prefiks E5
"passage: " secara individual.

Catatan perbaikan dari pipeline lama: sebelumnya prefiks "passage: "
ditempel ke seluruh teks satu HALAMAN sebelum di-split, sehingga hanya
chunk pertama dari halaman itu yang benar-benar berawalan "passage: " --
chunk berikutnya dari halaman yang sama kehilangan prefiksnya. Di sini
prefiks ditempel setelah chunking selesai, ke tiap chunk, supaya semua
chunk konsisten (simetris dengan prefiks "query: " di sisi pipeline.py).
"""

from typing import Any, Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.segmentation import Segment


def chunk_segments(
    segments: List[Segment],
    chunk_size: int,
    chunk_overlap: int,
    base_metadata: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Mengembalikan list dict chunk siap tulis ke chunks.jsonl:
      {"text": "passage: ...", "kategori":..., "jenis":..., "sumber":...,
       "unit":..., "halaman": <halaman_mulai_segmen>}

    Halaman yang dicatat per chunk adalah halaman_mulai segmennya --
    penyederhanaan yang disengaja karena satu Pasal jarang melewati lebih
    dari 1-2 halaman, dan tracking halaman per-sub-chunk butuh bookkeeping
    karakter-demi-karakter yang tidak sepadan manfaatnya untuk sitasi.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks: List[Dict[str, Any]] = []
    for segment in segments:
        pieces = splitter.split_text(segment.text)
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            chunks.append({
                "text": f"passage: {piece}",
                **base_metadata,
                "unit": segment.unit,
                "halaman": segment.halaman_mulai,
            })
    return chunks
