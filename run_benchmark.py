import os
import json
import pandas as pd
from pathlib import Path
from src.pipeline import WaqfRAGPipeline
from src.evaluator import (
    load_evaluation_set,
    run_blinded_responses_generation,
    evaluate_with_ragas
)
from src.config import RESULTS_DIR

def main():
    print("=" * 60)
    print("=== BENCHMARK EVALUASI RAG CHATBOT WAKAF PRODUKTIF ===")
    print("=" * 60)

    # 1. Pastikan API Keys terdeteksi
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not gemini_key and not openai_key:
        print("[WARNING] Tidak ditemukan GEMINI_API_KEY maupun OPENAI_API_KEY di environment.")
        print("[WARNING] Harap isi file .env terlebih dahulu untuk menjalankan generasi jawaban.")
        print("[INFO] Prosedur dihentikan demi menghindari error API.")
        return
        
    # 2. Inisialisasi pipeline RAG
    try:
        pipeline = WaqfRAGPipeline()
    except Exception as e:
        print(f"[ERROR] Gagal menginisialisasi pipeline RAG: {e}")
        return

    # 3. Muat kueri evaluasi
    try:
        eval_set = load_evaluation_set()
        print(f"[INFO] Berhasil memuat {len(eval_set)} skenario kueri dari dataset evaluasi.")
    except Exception as e:
        print(f"[ERROR] Gagal memuat dataset evaluasi: {e}")
        return

    # 4. Jalankan generasi 60 respons Blinded Eval
    df_responses = run_blinded_responses_generation(pipeline, eval_set)

    # 5. Jalankan Evaluasi Ragas
    ragas_results = {}
    
    # Gemini
    gemini_metrics = evaluate_with_ragas(df_responses, "Gemini 3.6 Flash")
    if gemini_metrics:
        ragas_results["Gemini 3.6 Flash"] = gemini_metrics
        
    # OpenAI
    openai_metrics = evaluate_with_ragas(df_responses, "GPT-4o Mini")
    if openai_metrics:
        ragas_results["GPT-4o Mini"] = openai_metrics

    # 6. Tampilkan dan simpan ringkasan hasil jika tersedia
    if ragas_results:
        # Simpan ringkasan ke JSON
        summary_path = RESULTS_DIR / "ragas_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(ragas_results, f, indent=4)
        print(f"\n[SUCCESS] Ringkasan metrik Ragas berhasil disimpan ke '{summary_path}'")
        
        # Buat tabel perbandingan sederhana untuk ditampilkan di terminal
        df_summary = pd.DataFrame(ragas_results).T
        print("\n" + "=" * 50)
        print("TABEL RINGKASAN METRIK EVALUASI RAGAS")
        print("=" * 50)
        print(df_summary.to_string())
        print("=" * 50)
    else:
        print("\n" + "=" * 60)
        print("[NOTE] Evaluasi Ragas dilewati/gagal.")
        print("Namun, file respons untuk Blinded Evaluation manual telah disimpan di:")
        print(f"  -> {RESULTS_DIR / 'blinded_evaluation_responses.csv'}")
        print("Silakan buka file tersebut untuk melihat dan menilai secara manual.")
        print("Untuk menjalankan penilaian Ragas otomatis, pastikan OPENAI_API_KEY diatur.")
        print("=" * 60)

if __name__ == "__main__":
    main()
