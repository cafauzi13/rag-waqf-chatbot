import os
import sys
from dotenv import load_dotenv

# Memastikan root directory ada dalam path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import WaqfRAGPipeline

def print_separator(char="=", length=60):
    print(char * length)

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

    # Pemilihan Model LLM
    print("\nPilih model generator LLM untuk sesi ini:")
    print("1. Gemini 3.6 Flash (Rekomendasi)")
    print("2. GPT-4o Mini")
    print("3. Bandingkan Keduanya (Gemini & OpenAI)")
    
    choice = input("Masukkan pilihan (1/2/3) [Default: 1]: ").strip()
    if choice == "2":
        model_choice = "openai"
        model_label = "GPT-4o Mini"
    elif choice == "3":
        model_choice = "compare"
        model_label = "Perbandingan Gemini & OpenAI"
    else:
        model_choice = "gemini"
        model_label = "Gemini 3.6 Flash"
        
    print(f"\n[OK] Model aktif: {model_label}")
    print("Ketik 'keluar' atau 'exit' untuk menghentikan obrolan.")
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
            
        print("\n⏳ Sedang mencari referensi dokumen dan memproses jawaban...")
        
        if model_choice == "compare":
            # Gemini Query
            print("\n\033[92m[GEMINI 3.6 FLASH]\033[0m")
            try:
                res_gemini = pipeline.query(query, model_choice="gemini")
                print(res_gemini["answer"])
            except Exception as e:
                print(f"Error Gemini: {e}")
                
            # OpenAI Query
            print("\n\033[93m[GPT-4o MINI]\033[0m")
            try:
                res_openai = pipeline.query(query, model_choice="openai")
                print(res_openai["answer"])
                res = res_openai # Ambil doc trace dari openai
            except Exception as e:
                print(f"Error OpenAI: {e}")
                res = res_gemini if 'res_gemini' in locals() else None
        else:
            try:
                res = pipeline.query(query, model_choice=model_choice)
                print(f"\n\033[92mAssistant ({model_label}) >\033[0m")
                print(res["answer"])
            except Exception as e:
                print(f"[ERROR] Gagal mendapatkan jawaban: {e}")
                res = None

        # Tampilkan trace dokumen
        if res and res.get("reranked_docs"):
            print("\n\033[90m" + "-" * 50)
            print("🔍 DOKUMEN PENDUKUNG (RAG Trace - Top 3 Re-ranked Chunks):")
            for idx, doc in enumerate(res["reranked_docs"]):
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "-")
                score = doc.metadata.get("rerank_score", 0.0)
                content = doc.page_content
                if content.startswith("passage: "):
                    content = content[len("passage: "):]
                print(f"  {idx+1}. [{source} - Hal. {page}] (Rerank Score: {score:.4f})")
                print(f"     \"{content[:150]}...\"")
            print("-" * 50 + "\033[0m")

if __name__ == "__main__":
    main()
