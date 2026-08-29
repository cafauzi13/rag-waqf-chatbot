import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

from datasets import Dataset
from ragas import evaluate
from ragas.llms import llm_factory
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from openai import OpenAI

from src.pipeline import WaqfRAGPipeline
from src.config import RESULTS_DIR, DATA_DIR, GEMINI_API_KEY, EMBEDDING_MODEL_NAME

def load_evaluation_set() -> List[Dict[str, str]]:
    """
    Memuat dataset evaluasi berisi kueri dan ground truth.
    """
    eval_file = DATA_DIR / "evaluation_set.json"
    if not eval_file.exists():
        raise FileNotFoundError(f"File dataset evaluasi tidak ditemukan di '{eval_file}'.")
    
    with open(eval_file, "r", encoding="utf-8") as f:
        return json.load(f)

def run_blinded_responses_generation(pipeline: WaqfRAGPipeline, eval_set: List[Dict[str, str]]) -> pd.DataFrame:
    """
    Menjalankan 30 query pada kedua model LLM (Gemini & OpenAI)
    sehingga menghasilkan total 60 respons untuk Blinded Evaluation.
    """
    print(f"[INFO] Memulai pembuatan 60 respons Blinded Eval (30 kueri x 2 model)...")
    
    records = []
    
    for i, item in enumerate(eval_set):
        qid = i + 1
        query_text = item["question"]
        ground_truth = item["ground_truth"]
        
        print(f"  [{qid}/{len(eval_set)}] Memproses kueri: '{query_text[:40]}...'")
        
        # 1. Jalankan untuk Gemini
        print("    - Menjalankan Gemini...")
        try:
            gemini_res = pipeline.query(query_text, model_choice="gemini")
            gemini_answer = gemini_res["answer"]
            gemini_contexts = [doc.page_content for doc in gemini_res["reranked_docs"]]
            # Hilangkan prefiks "passage: "
            gemini_contexts_clean = [c[len("passage: "):] if c.startswith("passage: ") else c for c in gemini_contexts]
        except Exception as e:
            gemini_answer = f"[ERROR] Gagal generasi Gemini: {e}"
            gemini_contexts_clean = []
            
        records.append({
            "query_id": qid,
            "question": query_text,
            "model_name": "Gemini 3.6 Flash",
            "answer": gemini_answer,
            "contexts": gemini_contexts_clean,
            "ground_truth": ground_truth
        })
        
        # 2. Jalankan untuk OpenAI (jika ada kuota)
        print("    - Menjalankan OpenAI...")
        try:
            openai_res = pipeline.query(query_text, model_choice="openai")
            openai_answer = openai_res["answer"]
            openai_contexts = [doc.page_content for doc in openai_res["reranked_docs"]]
            openai_contexts_clean = [c[len("passage: "):] if c.startswith("passage: ") else c for c in openai_contexts]
        except Exception as e:
            openai_answer = f"[ERROR] Gagal generasi OpenAI: {e}"
            openai_contexts_clean = []
            
        records.append({
            "query_id": qid,
            "question": query_text,
            "model_name": "GPT-4o Mini",
            "answer": openai_answer,
            "contexts": openai_contexts_clean,
            "ground_truth": ground_truth
        })

        # Memberikan jeda waktu 4 detik per kueri untuk menghindari rate limit pada Free Tier API Key (max 15 RPM)
        import time
        time.sleep(4)

    df = pd.DataFrame(records)
    output_path = RESULTS_DIR / "blinded_evaluation_responses.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[SUCCESS] Berhasil menyimpan 60 respons ke '{output_path}'")
    return df

def evaluate_with_ragas(df_model: pd.DataFrame, model_name: str) -> Optional[Dict[str, float]]:
    """
    Menjalankan evaluasi Ragas untuk subset model tertentu.
    Menggunakan Gemini 3.6 Flash sebagai Judge LLM dan HuggingFace Embeddings.
    """
    print(f"\n[INFO] Menjalankan evaluasi RAGAS untuk model: '{model_name}'...")
    
    # Filter data untuk model ini saja
    df_filtered = df_model[df_model["model_name"] == model_name].copy()
    
    # Periksa apakah ada error di kolom jawaban
    has_errors = df_filtered["answer"].str.startswith("[ERROR]").any()
    if has_errors:
        print(f"[WARNING] Evaluasi RAGAS untuk {model_name} dilewati karena terdapat error pada respons generasi.")
        return None

    # Siapkan dataset dalam format Ragas
    ragas_data = {
        "user_input": df_filtered["question"].tolist(),
        "retrieved_contexts": df_filtered["contexts"].tolist(),
        "response": df_filtered["answer"].tolist(),
        "reference": df_filtered["ground_truth"].tolist()
    }
    
    dataset = Dataset.from_dict(ragas_data)
    
    # Pastikan API key Gemini tersedia
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key:
        print("[WARNING] GEMINI_API_KEY tidak ditemukan untuk Evaluator Judge Ragas.")
        return None
        
    try:
        # Inisialisasi Evaluator LLM (Gemini via OpenAI-compatible endpoint)
        gemini_client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        evaluator_llm = llm_factory("gemini-3.6-flash", client=gemini_client)
        
        # Inisialisasi Embeddings untuk metrik relevansi
        evaluator_embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Jalankan Ragas Evaluation
        result = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall
            ],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings
        )
        
        # Hitung skor rata-rata
        df_result = result.to_pandas()
        metric_cols = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
        metrics_summary = {}
        for col in metric_cols:
            if col in df_result.columns:
                metrics_summary[col] = round(float(df_result[col].mean()), 4)
                
        print(f"[SUCCESS] Evaluasi RAGAS untuk {model_name} selesai.")
        print(json.dumps(metrics_summary, indent=2))
        return metrics_summary
    except Exception as e:
        print(f"[ERROR] Terjadi kegagalan saat menjalankan evaluasi Ragas untuk {model_name}: {e}")
        return None
