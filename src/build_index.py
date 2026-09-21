"""
src/build_index.py

Tahap 2 ingestion: baca data/processed/chunks.jsonl (dihasilkan
`python -m src.ingest`) -> embed -> simpan indeks FAISS. Dipisah dari
src/ingest.py supaya ganti model embedding atau eksperimen ulang indexing
tidak perlu re-ekstraksi & re-cleaning seluruh PDF dari awal -- chunks.jsonl
adalah checkpoint yang bisa dipakai ulang.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import EMBEDDING_MODEL_NAME, FAISS_INDEX_DIR
from src.ingest import CHUNKS_JSONL_PATH


def load_chunks_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"'{path}' tidak ditemukan. Jalankan `python -m src.ingest` dulu untuk menghasilkannya."
        )
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def chunks_to_documents(chunks: List[Dict[str, Any]]) -> List[Document]:
    documents = []
    for chunk in chunks:
        metadata = {k: v for k, v in chunk.items() if k != "text"}
        documents.append(Document(page_content=chunk["text"], metadata=metadata))
    return documents


def build_faiss_vectorstore(documents: List[Document], save_dir: Path) -> None:
    print(f"[INFO] Menginisialisasi model embedding '{EMBEDDING_MODEL_NAME}'...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print(f"[INFO] Membangun indeks FAISS dari {len(documents)} dokumen...")
    vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)

    print(f"[INFO] Menyimpan indeks FAISS ke '{save_dir}'...")
    vectorstore.save_local(str(save_dir))
    print("[SUCCESS] Indeks FAISS lokal berhasil disimpan dan siap digunakan!")


def main():
    print("=== TAHAP 2: chunks.jsonl -> Indeks FAISS ===")
    chunks = load_chunks_jsonl(CHUNKS_JSONL_PATH)
    print(f"[INFO] Memuat {len(chunks)} chunk dari '{CHUNKS_JSONL_PATH}'.")
    documents = chunks_to_documents(chunks)
    build_faiss_vectorstore(documents, FAISS_INDEX_DIR)
    print("=== SELESAI ===")


if __name__ == "__main__":
    main()
