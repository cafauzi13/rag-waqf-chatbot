import pandas as pd
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import FAISS_INDEX_DIR, EMBEDDING_MODEL_NAME, PROCESSED_DATA_DIR

def main():
    print("[INFO] Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print(f"[INFO] Loading FAISS index from '{FAISS_INDEX_DIR}'...")
    try:
        vectorstore = FAISS.load_local(
            str(FAISS_INDEX_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"[ERROR] Gagal memuat indeks FAISS: {e}")
        return

    # Mengambil semua dokumen dari docstore FAISS
    docstore = vectorstore.docstore
    docs = list(docstore._dict.values())
    
    print(f"[INFO] Ditemukan {len(docs)} chunks di dalam FAISS database.")
    
    # Membuat list data untuk diekspor
    data = []
    for i, doc in enumerate(docs):
        # Menghapus prefiks "passage: " untuk tampilan debug yang lebih bersih
        content_clean = doc.page_content
        if content_clean.startswith("passage: "):
            content_clean = content_clean[len("passage: "):]
            
        data.append({
            "chunk_id": i + 1,
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", "-"),
            "character_length": len(content_clean),
            "content": content_clean
        })
        
    df = pd.DataFrame(data)
    
    # Simpan ke CSV di folder data/processed
    output_path = PROCESSED_DATA_DIR / "extracted_chunks.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    
    print(f"[SUCCESS] Berhasil mengekspor chunks ke '{output_path}'!")
    print(f"[INFO] Anda dapat membuka file tersebut untuk memeriksa isi teks hasil ekstraksi.")

if __name__ == "__main__":
    main()
