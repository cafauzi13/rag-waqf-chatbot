from typing import List
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from src.config import RERANKER_MODEL_NAME

class WaqfReranker:
    """
    Modul Re-ranker menggunakan model Cross-Encoder mixedbread-ai/mxbai-rerank-base-v2
    untuk menilai kecocokan dokumen hasil retrieval awal dengan kueri.
    """
    def __init__(self, model_name: str = RERANKER_MODEL_NAME, device: str = "cpu"):
        print(f"[INFO] Inisialisasi Re-ranker dengan model '{model_name}' pada device '{device}'...")
        self.model = CrossEncoder(model_name, device=device)

    def rerank(self, query: str, documents: List[Document], top_k: int) -> List[Document]:
        """
        Melakukan perankingan ulang terhadap dokumen berdasarkan relevansinya dengan kueri.
        """
        if not documents:
            print("[WARNING] Tidak ada dokumen yang diberikan untuk proses Re-rank.")
            return []

        # Menyiapkan pasangan input (kueri, isi dokumen)
        # Catatan: Kita gunakan doc.page_content. 
        # Jika teks memiliki prefiks "passage: ", kita gunakan teks bersih untuk perbandingan yang lebih baik,
        # tetapi mxbai-rerank juga sangat robust terhadap teks asli.
        pairs = []
        for doc in documents:
            text = doc.page_content
            # Menghapus prefiks "passage: " jika ada untuk keperluan reranking agar lebih bersih
            if text.startswith("passage: "):
                text = text[len("passage: "):]
            pairs.append((query, text))

        print(f"[INFO] Melakukan re-ranking terhadap {len(documents)} dokumen...")
        scores = self.model.predict(pairs)

        # Memasukkan skor rerank ke dalam metadata dokumen
        for doc, score in zip(documents, scores):
            doc.metadata["rerank_score"] = float(score)

        # Mengurutkan dokumen berdasarkan skor rerank tertinggi
        ranked_documents = sorted(
            documents, 
            key=lambda x: x.metadata["rerank_score"], 
            reverse=True
        )

        print(f"[SUCCESS] Re-ranking selesai. Memilih top-{min(top_k, len(ranked_documents))} dokumen.")
        return ranked_documents[:top_k]
