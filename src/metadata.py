"""
src/metadata.py

Turunkan metadata kategori/jenis/sumber dari posisi file PDF relatif
terhadap data/raw/<kategori>/<jenis>/<file>.pdf. Sengaja berbasis STRUKTUR
FOLDER (bukan parsing nama file) supaya tetap benar terlepas dari skema
penamaan file yang dipakai.
"""

from pathlib import Path
from typing import TypedDict


class PathMetadata(TypedDict):
    kategori: str
    jenis: str
    sumber: str


def derive_metadata_from_path(pdf_path: Path, raw_dir: Path) -> PathMetadata:
    """
    pdf_path: data/raw/wakaf/regulasi/WKF-REG-01_UU-41-2004.pdf
    raw_dir:  data/raw
    -> {"kategori": "wakaf", "jenis": "regulasi", "sumber": "WKF-REG-01_UU-41-2004.pdf"}
    """
    rel_parts = pdf_path.resolve().relative_to(raw_dir.resolve()).parts
    if len(rel_parts) < 3:
        raise ValueError(
            f"'{pdf_path}' tidak berada di struktur data/raw/<kategori>/<jenis>/<file>.pdf yang diharapkan."
        )
    kategori, jenis = rel_parts[0], rel_parts[1]
    return {"kategori": kategori, "jenis": jenis, "sumber": pdf_path.name}
