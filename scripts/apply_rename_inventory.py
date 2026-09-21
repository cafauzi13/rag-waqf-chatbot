"""
scripts/apply_rename_inventory.py

Eksekusi rename fisik berdasarkan results/inventaris_draft.xlsx yang sudah
final (hasil review manual penulis). Untuk tiap baris: rename
data/raw/{folder}/{nama_lama} -> data/raw/{folder}/{nama_baru_usulan}.

Aman dijalankan ulang (idempoten): baris yang nama_lama-nya sudah tidak ada
(berarti sudah pernah di-rename sebelumnya) dilewati, bukan dianggap error.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import RAW_DATA_DIR, RESULTS_DIR

INVENTORY_PATH = RESULTS_DIR / "inventaris_draft.xlsx"


def main():
    df = pd.read_excel(INVENTORY_PATH)

    renamed, skipped, errors = 0, 0, []

    for _, row in df.iterrows():
        folder = row["folder"]
        old_name = row["nama_lama"]
        new_name = row["nama_baru_usulan"]

        old_path = RAW_DATA_DIR / folder / old_name
        new_path = RAW_DATA_DIR / folder / new_name

        if new_path.exists() and not old_path.exists():
            skipped += 1
            continue

        if not old_path.exists():
            errors.append(f"[TIDAK DITEMUKAN] {old_path}")
            continue

        if new_path.exists() and old_path != new_path:
            errors.append(f"[TARGET SUDAH ADA] {new_path} (dari {old_name})")
            continue

        old_path.rename(new_path)
        print(f"  {folder}/{old_name}\n    -> {new_name}")
        renamed += 1

    print(f"\n[SUCCESS] {renamed} file di-rename, {skipped} sudah sesuai (dilewati).")
    if errors:
        print(f"[WARNING] {len(errors)} masalah:")
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
