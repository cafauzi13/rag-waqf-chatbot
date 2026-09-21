# inventaris_korpus.py
# Jalankan: python inventaris_korpus.py <folder_korpus>
# Butuh: pip install pymupdf
import sys, re
from pathlib import Path
import fitz

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out = []
for pdf in sorted(root.rglob("*.pdf")):
    try:
        doc = fitz.open(pdf)
        text = " ".join(page.get_text() for page in doc)
        text = re.sub(r"\s+", " ", text).strip()
        rel = pdf.relative_to(root).as_posix()
        out.append(f"{rel}\t{doc.page_count} hlm\t{len(text.split())} kata\t{text[:250]}")
    except Exception as e:
        out.append(f"{pdf.relative_to(root).as_posix()}\tERROR: {e}")

Path("inventaris_korpus.txt").write_text(
    "path\thalaman\tkata\tcuplikan_awal\n" + "\n".join(out), encoding="utf-8")
print(f"{len(out)} dokumen -> inventaris_korpus.txt")
