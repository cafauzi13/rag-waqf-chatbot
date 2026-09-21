"""
Script pengujian latency untuk pipeline RAG WaqfRAG, khusus mode Ollama lokal.

Mengukur waktu tiap tahap secara terpisah dengan memanggil langsung
komponen internal WaqfRAGPipeline (bukan lewat pipeline.query() secara utuh),
mengikuti struktur asli di src/pipeline.py dan src/reranker.py:
    - pipeline.embeddings.embed_query(...)          -> embedding kueri
    - pipeline.vectorstore.similarity_search_with_score_by_vector(...) -> retrieval FAISS
    - pipeline.reranker.rerank(...)                 -> reranking
    - pipeline.get_ollama_llm().invoke(...)          -> generasi jawaban LLM

Dijalankan 3 kali berturut-turut dalam satu proses agar terlihat perbedaan
cold start (run pertama, termasuk lazy-load model Ollama) vs warm run.
"""

import time
from src.pipeline import WaqfRAGPipeline
from langchain_core.documents import Document

TEST_QUERY = "Apa itu wakaf uang?"
TOTAL_RUNS = 3


def run_single_query(pipeline: WaqfRAGPipeline, user_query: str) -> dict:
    """
    Menjalankan satu query melalui tahap-tahap RAG secara manual (bukan lewat
    pipeline.query()) supaya waktu tiap tahap bisa diukur terpisah.
    """
    timings = {}

    # --- [1] Embedding Kueri ---
    query_formatted = f"query: {user_query}"
    t0 = time.time()
    query_vector = pipeline.embeddings.embed_query(query_formatted)
    timings["embedding"] = time.time() - t0

    # --- [2] Retrieval FAISS (top-K, sesuai TOP_K_RETRIEVAL) ---
    t0 = time.time()
    docs_and_scores = pipeline.vectorstore.similarity_search_with_score_by_vector(
        query_vector,
        k=pipeline.top_k_retrieval
    )
    timings["retrieval"] = time.time() - t0

    retrieved_docs = []
    for doc, score in docs_and_scores:
        doc_copy = Document(page_content=doc.page_content, metadata=doc.metadata.copy())
        doc_copy.metadata["similarity_score"] = float(score)
        retrieved_docs.append(doc_copy)

    # --- [3] Reranking (top-K, sesuai TOP_K_RERANK) ---
    t0 = time.time()
    reranked_docs = pipeline.reranker.rerank(
        user_query,
        retrieved_docs,
        top_k=pipeline.top_k_rerank
    )
    timings["reranking"] = time.time() - t0

    # --- Bangun prompt konteks (sama seperti di pipeline.query()) ---
    context_items = []
    for i, doc in enumerate(reranked_docs):
        content = doc.page_content
        if content.startswith("passage: "):
            content = content[len("passage: "):]
        source_info = f"[Sumber: {doc.metadata.get('sumber') or doc.metadata.get('source', 'Tidak Diketahui')}, Hal: {doc.metadata.get('halaman') or doc.metadata.get('page', '-')}]"
        context_items.append(f"Dokumen {i+1} {source_info}:\n{content.strip()}")
    context_str = "\n\n".join(context_items)
    prompt_str = pipeline.prompt_template.format(context=context_str, question=user_query)

    # --- [4] Generasi Jawaban via LLM (Ollama) ---
    t0 = time.time()
    llm = pipeline.get_ollama_llm()
    response = llm.invoke(prompt_str)
    timings["llm_generation"] = time.time() - t0

    answer = response.content if isinstance(response.content, str) else str(response.content)

    timings["total"] = (
        timings["embedding"]
        + timings["retrieval"]
        + timings["reranking"]
        + timings["llm_generation"]
    )
    timings["answer"] = answer
    timings["num_retrieved"] = len(retrieved_docs)
    timings["num_reranked"] = len(reranked_docs)
    return timings


def print_result(run_idx: int, timings: dict) -> None:
    label = "COLD START" if run_idx == 1 else "WARM"
    print(f"\n===== RUN {run_idx} ({label}) =====")
    print(f"[1] Embedding Query      : {timings['embedding']:.2f} detik")
    print(f"[2] FAISS Retrieval      : {timings['retrieval']:.2f} detik  ({timings['num_retrieved']} dokumen)")
    print(f"[3] Reranking            : {timings['reranking']:.2f} detik  ({timings['num_reranked']} dokumen)")
    print(f"[4] LLM Generation       : {timings['llm_generation']:.2f} detik")
    print("-" * 40)
    print(f"TOTAL                    : {timings['total']:.2f} detik")
    print(f"\nJawaban: {timings['answer']}")


def main():
    print(f"[SETUP] Memuat WaqfRAGPipeline (di luar pengukuran waktu)...")
    setup_start = time.time()
    pipeline = WaqfRAGPipeline()
    setup_elapsed = time.time() - setup_start
    print(f"[SETUP] Pipeline siap dalam {setup_elapsed:.2f} detik.\n")

    print(f"Query uji: \"{TEST_QUERY}\"")
    print(f"Mode LLM: Ollama (lokal) | Jumlah run: {TOTAL_RUNS}")

    all_timings = []
    for i in range(1, TOTAL_RUNS + 1):
        timings = run_single_query(pipeline, TEST_QUERY)
        print_result(i, timings)
        all_timings.append(timings)

    # --- Ringkasan Perbandingan Antar-Run ---
    print("\n\n===== RINGKASAN SEMUA RUN =====")
    header = f"{'Run':<6}{'Embedding':<12}{'Retrieval':<12}{'Reranking':<12}{'LLM Gen':<12}{'Total':<10}"
    print(header)
    print("-" * len(header))
    for i, t in enumerate(all_timings, start=1):
        print(
            f"{i:<6}{t['embedding']:<12.2f}{t['retrieval']:<12.2f}"
            f"{t['reranking']:<12.2f}{t['llm_generation']:<12.2f}{t['total']:<10.2f}"
        )


if __name__ == "__main__":
    main()
