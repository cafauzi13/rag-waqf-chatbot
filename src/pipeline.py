import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.config import (
    FAISS_INDEX_DIR,
    EMBEDDING_MODEL_NAME,
    LLM_GEMINI_NAME,
    LLM_OPENAI_NAME,
    TEMPERATURE,
    TOP_K_RETRIEVAL,
    TOP_K_RERANK,
    GEMINI_API_KEY,
    OPENAI_API_KEY
)
from src.reranker import WaqfReranker

class WaqfRAGPipeline:
    """
    RAG Pipeline untuk mengintegrasikan proses retrieval, re-ranking, dan generasi jawaban.
    """
    def __init__(self, top_k_retrieval: int = TOP_K_RETRIEVAL, top_k_rerank: int = TOP_K_RERANK):
        self.top_k_retrieval = top_k_retrieval
        self.top_k_rerank = top_k_rerank
        
        # 1. Inisialisasi Model Embedding
        print(f"[INFO] Pipeline: Memuat model embedding '{EMBEDDING_MODEL_NAME}'...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # 2. Memuat Vectorstore FAISS lokal
        print(f"[INFO] Pipeline: Memuat FAISS index dari '{FAISS_INDEX_DIR}'...")
        try:
            self.vectorstore = FAISS.load_local(
                str(FAISS_INDEX_DIR),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("[SUCCESS] Pipeline: FAISS index berhasil dimuat.")
        except Exception as e:
            print(f"[ERROR] Pipeline: Gagal memuat FAISS index: {e}")
            self.vectorstore = None

        # 3. Inisialisasi Re-ranker
        self.reranker = WaqfReranker()

        # 4. Prompt Template Berbahasa Indonesia sesuai ketentuan proposal
        self.prompt_template = (
            "Anda adalah asisten AI ahli dalam bidang Wakaf Produktif di Indonesia.\n"
            "Tugas Anda adalah menjawab pertanyaan pengguna secara akurat, objektif, dan hanya berdasarkan konteks dokumen wakaf produktif yang disediakan di bawah ini.\n\n"
            "Konteks Dokumen:\n"
            "{context}\n\n"
            "Pertanyaan: {question}\n\n"
            "Aturan Jawaban:\n"
            "1. Jawablah pertanyaan hanya berdasarkan fakta-fakta yang tertulis di dalam Konteks Dokumen.\n"
            "2. Jangan menambahkan informasi di luar dokumen, spekulasi, atau interpretasi pribadi.\n"
            "3. Jika informasi untuk menjawab pertanyaan TIDAK terdapat dalam Konteks Dokumen yang diberikan, maka Anda wajib menjawab persis seperti ini:\n"
            "   \"Maaf, informasi tidak ditemukan dalam dokumen wakaf produktif yang tersedia.\"\n"
            "4. Tuliskan jawaban Anda secara ringkas, profesional, dan dalam Bahasa Indonesia yang baik dan benar.\n\n"
            "Jawaban:"
        )

        # Caching instansi LLM agar tidak dibuat berulang kali
        self._gemini_llm = None
        self._openai_llm = None

    def get_gemini_llm(self) -> ChatGoogleGenerativeAI:
        if not self._gemini_llm:
            api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
            if not api_key:
                raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variable atau .env")
            print(f"[INFO] Pipeline: Menginisialisasi Gemini LLM ({LLM_GEMINI_NAME})...")
            self._gemini_llm = ChatGoogleGenerativeAI(
                model=LLM_GEMINI_NAME,
                google_api_key=api_key,
                temperature=TEMPERATURE
            )
        return self._gemini_llm

    def get_openai_llm(self) -> ChatOpenAI:
        if not self._openai_llm:
            api_key = os.getenv("OPENAI_API_KEY") or OPENAI_API_KEY
            if not api_key:
                raise ValueError("OPENAI_API_KEY tidak ditemukan di environment variable atau .env")
            print(f"[INFO] Pipeline: Menginisialisasi OpenAI LLM ({LLM_OPENAI_NAME})...")
            self._openai_llm = ChatOpenAI(
                model=LLM_OPENAI_NAME,
                api_key=api_key,
                temperature=TEMPERATURE
            )
        return self._openai_llm

    def query(self, user_query: str, model_choice: str = "gemini") -> Dict[str, Any]:
        """
        Menjalankan query melalui alur RAG lengkap:
        1. Format kueri dengan prefiks "query: "
        2. Pencarian awal menggunakan FAISS (top-10) beserta skor jarak
        3. Re-ranking dokumen menggunakan Cross-Encoder (top-3)
        4. Pembuatan prompt konteks
        5. Generasi jawaban via LLM (Gemini atau OpenAI)
        """
        if not self.vectorstore:
            return {
                "answer": "Error: Database FAISS belum siap atau gagal dimuat.",
                "retrieved_docs": [],
                "reranked_docs": [],
                "prompt": ""
            }

        # 1. Format kueri untuk model E5 (rekomendasi menyertakan "query: ")
        query_formatted = f"query: {user_query}"
        
        # 2. Similarity search di FAISS dengan skor (L2 distance / inner product)
        print(f"[INFO] Pipeline: Mencari dokumen relevan untuk: '{user_query}'...")
        docs_and_scores = self.vectorstore.similarity_search_with_score(
            query_formatted, 
            k=self.top_k_retrieval
        )
        
        retrieved_docs = []
        for doc, score in docs_and_scores:
            # Duplikasi dokumen agar tidak mengotori cache
            doc_copy = Document(page_content=doc.page_content, metadata=doc.metadata.copy())
            # Jarak FAISS L2 (semakin kecil nilainya semakin mirip)
            doc_copy.metadata["similarity_score"] = float(score)
            retrieved_docs.append(doc_copy)
            
        print(f"[SUCCESS] Pipeline: Menemukan {len(retrieved_docs)} dokumen dari FAISS.")

        # 3. Proses Re-ranking (top-10 -> top-3)
        reranked_docs = self.reranker.rerank(user_query, retrieved_docs, top_k=self.top_k_rerank)

        # 4. Bangun konteks teks untuk prompt
        context_items = []
        for i, doc in enumerate(reranked_docs):
            content = doc.page_content
            # Hilangkan prefiks "passage: " jika ada agar prompt bersih
            if content.startswith("passage: "):
                content = content[len("passage: "):]
            
            source_info = f"[Sumber: {doc.metadata.get('source', 'Tidak Diketahui')}, Hal: {doc.metadata.get('page', '-')}]"
            context_items.append(f"Dokumen {i+1} {source_info}:\n{content.strip()}")
            
        context_str = "\n\n".join(context_items)

        # 5. Bangun Prompt Lengkap
        prompt_str = self.prompt_template.format(context=context_str, question=user_query)

        # 6. Generasi Jawaban
        model_choice_clean = model_choice.lower().strip()
        print(f"[INFO] Pipeline: Menghasilkan jawaban menggunakan model LLM: '{model_choice_clean}'...")
        
        try:
            if model_choice_clean == "gemini":
                llm = self.get_gemini_llm()
            elif model_choice_clean == "openai":
                llm = self.get_openai_llm()
            else:
                raise ValueError(f"Pilihan model generator '{model_choice}' tidak dikenal (gunakan 'gemini' atau 'openai').")
            
            response = llm.invoke(prompt_str)
            raw_content = response.content
            if isinstance(raw_content, list):
                text_parts = []
                for part in raw_content:
                    if isinstance(part, dict) and "text" in part:
                        text_parts.append(part["text"])
                    elif isinstance(part, str):
                        text_parts.append(part)
                answer = "".join(text_parts)
            else:
                answer = str(raw_content)
            print("[SUCCESS] Pipeline: Jawaban berhasil dihasilkan.")
        except Exception as e:
            print(f"[ERROR] Pipeline: Gagal melakukan generasi jawaban: {e}")
            answer = f"Error dalam proses generasi jawaban oleh LLM ({model_choice_clean}): {str(e)}"

        return {
            "answer": answer,
            "retrieved_docs": retrieved_docs,
            "reranked_docs": reranked_docs,
            "prompt": prompt_str
        }
