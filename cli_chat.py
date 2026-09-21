import os
import sys
from dotenv import load_dotenv

# Memastikan root directory ada dalam path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import WaqfRAGPipeline

def print_separator(char="=", length=60):
    print(char * length)

def select_model() -> tuple:
    """
    Menampilkan menu pemilihan model LLM dan mengembalikan (model_choice, model_label).
    Dipisah jadi fungsi sendiri supaya bisa dipanggil ulang di tengah sesi chat
    (perintah 'model') tanpa perlu memuat ulang pipeline (embedding + FAISS).
    """
    print("\nPilih model generator LLM untuk sesi ini:")
    print("1. Gemini 3.6 Flash (Rekomendasi)")
    print("2. GPT-4o Mini")
    print("3. Bandingkan Keduanya (Gemini & OpenAI)")
    print("4. Llama 3.2 (Ollama - Lokal, tanpa API key)")

    choice = input("Masukkan pilihan (1/2/3/4) [Default: 1]: ").strip()
    if choice == "2":
        model_choice, model_label = "openai", "GPT-4o Mini"
    elif choice == "3":
        model_choice, model_label = "compare", "Perbandingan Gemini & OpenAI"
    elif choice == "4":
        model_choice, model_label = "ollama", "Llama 3.2 (Ollama - Lokal)"
    else:
        model_choice, model_label = "gemini", "Gemini 3.6 Flash"

    print(f"[OK] Model aktif: {model_label}")
    return model_choice, model_label

def select_scenario() -> tuple:
    """
    Menampilkan menu pemilihan skenario RAG dan mengembalikan
    ((use_retrieval, use_rerank), scenario_label). Dipisah jadi fungsi
    sendiri dengan alasan yang sama seperti select_model() -- supaya bisa
    dipanggil ulang di tengah sesi lewat perintah 'skenario'.
    """
    print("\nPilih skenario RAG untuk sesi ini:")
    print("1. LLM saja (tanpa RAG) - baseline")
    print("2. RAG tanpa Re-ranking (10 dokumen)")
    print("3. RAG dengan Re-ranking (3 dokumen) - Rekomendasi")

    scenario_choice = input("Masukkan pilihan (1/2/3) [Default: 3]: ").strip()
    if scenario_choice == "1":
        scenario, scenario_label = (False, False), "LLM Saja (Baseline, tanpa RAG)"
    elif scenario_choice == "2":
        scenario, scenario_label = (True, False), "RAG tanpa Re-ranking (10 dokumen)"
    else:
        scenario, scenario_label = (True, True), "RAG dengan Re-ranking (3 dokumen)"

    print(f"[OK] Skenario aktif: {scenario_label}")
    return scenario, scenario_label

def main():
    # Load environment variables
    load_dotenv()
    
    print_separator()
    print("=== INTERACTIVE WAQFRAG CHATBOT TERMINAL ===")
    print_separator()
    print("[INFO] Sedang memuat model embedding dan indeks FAISS...")
    print("[INFO] Harap tunggu sebentar...")
    
    try:
        pipeline = WaqfRAGPipeline()
        print("\n[SUCCESS] Pipeline RAG berhasil dimuat!")
    except Exception as e:
        print(f"\n[ERROR] Gagal memuat RAG Pipeline: {e}")
        return

    # Pemilihan Model LLM & Skenario RAG awal
    model_choice, model_label = select_model()
    scenario, scenario_label = select_scenario()

    print("\nKetik 'keluar'/'exit' untuk berhenti, 'model' untuk ganti model,")
    print("atau 'skenario' untuk ganti skenario RAG -- tanpa perlu muat ulang pipeline.")
    print_separator(char="-")

    while True:
        try:
            query = input("\n\033[94mUser > \033[0m").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSesi dihentikan.")
            break

        if not query:
            continue

        if query.lower() in ["keluar", "exit", "quit"]:
            print("Sesi dihentikan. Terima kasih!")
            break

        # Perintah ganti model/skenario di tengah sesi -- memanggil ulang menu
        # yang sama seperti di awal, TAPI tidak menyentuh `pipeline` sama sekali
        # (embedding model + FAISS index tetap yang sudah dimuat), jadi tidak
        # perlu tunggu loading ulang cuma untuk ganti model/skenario pembanding.
        if query.lower() in ["model", "ganti model"]:
            model_choice, model_label = select_model()
            continue

        if query.lower() in ["skenario", "scenario", "ganti skenario"]:
            scenario, scenario_label = select_scenario()
            continue

        print("\n⏳ Sedang mencari referensi dokumen dan memproses jawaban...")
        
        use_retrieval, use_rerank = scenario

        if model_choice == "compare":
            # Gemini Query
            print("\n\033[92m[GEMINI 3.6 FLASH]\033[0m")
            try:
                res_gemini = pipeline.query(query, model_choice="gemini", use_retrieval=use_retrieval, use_rerank=use_rerank)
                print(res_gemini["answer"])
            except Exception as e:
                print(f"Error Gemini: {e}")

            # OpenAI Query
            print("\n\033[93m[GPT-4o MINI]\033[0m")
            try:
                res_openai = pipeline.query(query, model_choice="openai", use_retrieval=use_retrieval, use_rerank=use_rerank)
                print(res_openai["answer"])
                res = res_openai # Ambil doc trace dari openai
            except Exception as e:
                print(f"Error OpenAI: {e}")
                res = res_gemini if 'res_gemini' in locals() else None
        else:
            try:
                res = pipeline.query(query, model_choice=model_choice, use_retrieval=use_retrieval, use_rerank=use_rerank)
                print(f"\n\033[92mAssistant ({model_label}) >\033[0m")
                print(res["answer"])
            except Exception as e:
                print(f"[ERROR] Gagal mendapatkan jawaban: {e}")
                res = None

        # Tampilkan trace dokumen -- tampilannya dicabangkan berdasarkan
        # use_retrieval/use_rerank yang aktif, karena tiap kombinasi mengisi
        # retrieved_docs/reranked_docs secara berbeda (lihat src/pipeline.py):
        #   - use_retrieval=False            : retrieved_docs & reranked_docs
        #                                       sengaja kosong (LLM saja tanpa RAG).
        #   - use_retrieval=True, rerank=False: reranked_docs sengaja kosong,
        #                                       dokumen yang ada adalah retrieved_docs
        #                                       (top-10 FAISS, BELUM di-rerank).
        #   - use_retrieval=True, rerank=True : reranked_docs (top-3) dengan rerank_score.
        if res:
            print("\n\033[90m" + "-" * 50)
            if not use_retrieval:
                print("🔍 RAG Trace: [Tidak ada dokumen -- skenario LLM saja tanpa RAG]")
            elif not use_rerank:
                docs = res.get("retrieved_docs") or []
                print(f"🔍 DOKUMEN PENDUKUNG (RAG Trace - {len(docs)} Dokumen Hasil Retrieval, BELUM Di-rerank):")
                for idx, doc in enumerate(docs):
                    source = doc.metadata.get("sumber") or doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("halaman") or doc.metadata.get("page", "-")
                    score = doc.metadata.get("similarity_score", 0.0)
                    content = doc.page_content
                    if content.startswith("passage: "):
                        content = content[len("passage: "):]
                    print(f"  {idx+1}. [{source} - Hal. {page}] (FAISS Similarity Score: {score:.4f})")
                    print(f"     \"{content[:150]}...\"")
            else:
                docs = res.get("reranked_docs") or []
                print("🔍 DOKUMEN PENDUKUNG (RAG Trace - Top 3 Re-ranked Chunks):")
                for idx, doc in enumerate(docs):
                    source = doc.metadata.get("sumber") or doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("halaman") or doc.metadata.get("page", "-")
                    score = doc.metadata.get("rerank_score", 0.0)
                    content = doc.page_content
                    if content.startswith("passage: "):
                        content = content[len("passage: "):]
                    print(f"  {idx+1}. [{source} - Hal. {page}] (Rerank Score: {score:.4f})")
                    print(f"     \"{content[:150]}...\"")
            print("-" * 50 + "\033[0m")

if __name__ == "__main__":
    main()
