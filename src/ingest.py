import os
import re
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import (
    RAW_DATA_DIR,
    FAISS_INDEX_DIR,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


def clean_text(text: str) -> str:
    """
    Membersihkan teks hasil ekstraksi PDF dari header, footer,
    serta karakter non-semantik berulang.
    """
    # 1. Menghapus elemen navigasi/menu web yang sering terbawa dari unduhan BWI
    text = re.sub(r'Bahasa Indonesia\s*[▼▲]?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Konsultasi Wakaf', '', text, flags=re.IGNORECASE)
    text = re.sub(r'LITERASI WAKAF\s*–?', '', text, flags=re.IGNORECASE)
    
    # 2. Menghapus simbol khusus / icon font web yang sering muncul (misal: )
    text = re.sub(r'[\ue800-\uefff]', '', text)
    text = re.sub(r'[▼▲]', '', text)
    
    # 3. Menghapus baris yang HANYA berisi nomor halaman (misal baris berisi angka saja)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # 4. Menghapus multiple newlines dan spasi berlebih
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 5. Menghapus garis pemisah atau karakter tidak esensial
    text = re.sub(r'[-_]{3,}', '', text)
    
    return text.strip()


def load_and_preprocess_pdfs(raw_dir: Path) -> List[Document]:
    """
    Membaca seluruh file PDF regulasi dan korpus BWI dari folder data/raw,
    melakukan pembersihan teks, dan menyertakan metadata sumber.
    """
    pdf_files = list(raw_dir.rglob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"Tidak ditemukan file PDF di folder '{raw_dir}'.")

    print(f"[INFO] Ditemukan {len(pdf_files)} file PDF di '{raw_dir}'. Memulai pemuatan...")
    
    cleaned_documents = []
    
    for pdf_path in pdf_files:
        print(f"  - Memproses: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        
        for doc in docs:
            # Cleaning isi teks per halaman
            cleaned_content = clean_text(doc.page_content)
            
            if len(cleaned_content) > 20:  # Abaikan halaman kosong/derau
                # Menyimpan metadata lengkap untuk penelusuran balik (traceability)
                metadata = {
                    "source": pdf_path.name,
                    "page": doc.metadata.get("page", 0) + 1,
                    "file_path": str(pdf_path)
                }
                
                # Model E5 merekomendasikan penambahan awalan "passage: " pada dokumen corpus
                formatted_content = f"passage: {cleaned_content}"
                
                cleaned_documents.append(
                    Document(page_content=formatted_content, metadata=metadata)
                )

    print(f"[SUCCESS] Total {len(cleaned_documents)} halaman PDF berhasil diproses.")
    return cleaned_documents


def create_chunks(documents: List[Document]) -> List[Document]:
    """
    Memotong dokumen menjadi chunks berukuran 800 karakter dengan overlap 80 karakter.
    """
    print(f"[INFO] Melakukan chunking (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\nPasal", "\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"[SUCCESS] Dihasilkan total {len(chunks)} chunks.")
    return chunks


def build_faiss_vectorstore(chunks: List[Document], save_dir: Path) -> None:
    """
    Mengonversi chunks ke vektor menggunakan intfloat/multilingual-e5-base
    dan menyimpannya ke database vektor FAISS lokal.
    """
    print(f"[INFO] Menginisialisasi model embedding '{EMBEDDING_MODEL_NAME}'...")
    
    # Model kwargs & encode kwargs untuk normalisasi vektor (Cosine Similarity)
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    print("[INFO] Membangun indeks FAISS...")
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    
    print(f"[INFO] Menyimpan indeks FAISS ke '{save_dir}'...")
    vectorstore.save_local(str(save_dir))
    print("[SUCCESS] Indeks FAISS lokal berhasil disimpan dan siap digunakan!")


def main():
    print("=== MULAIPROSES INGESTION DATASET WAKAF PRODUKTIF ===")
    
    # 1. Pemuatan dan pra-pemrosesan PDF
    raw_docs = load_and_preprocess_pdfs(RAW_DATA_DIR)
    
    # 2. Chunking dokumen
    chunked_docs = create_chunks(raw_docs)
    
    # 3. Embedding dan Penyimpanan ke FAISS
    build_faiss_vectorstore(chunked_docs, FAISS_INDEX_DIR)
    
    print("=== PROSES INGESTION SELESAI ===")


if __name__ == "__main__":
    main()