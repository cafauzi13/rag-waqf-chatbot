"""
scripts/run_qa_batch.py

Jalankan daftar pertanyaan tetap lewat WaqfRAGPipeline (skenario RAG + Rerank,
model Gemini) dan simpan jawaban + dokumen rujukan ke file markdown di results/.
"""

import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.pipeline import WaqfRAGPipeline
from src.config import RESULTS_DIR, LLM_GEMINI_NAME

MODEL_CHOICE = "gemini"
USE_RETRIEVAL, USE_RERANK = True, True  # skenario RAG + Rerank
OUTPUT_PATH = RESULTS_DIR / "qa_batch_nazhir_wakaf_uang.md"

DELAY_BETWEEN_CALLS_SEC = 4

QUESTIONS = [
    "Nazhir itu tugasnya apa?",
    "Wakaf uang itu maksudnya gimana?",
    "Wakaf uang itu sebenarnya boleh nggak sih menurut hukum Islam?",
    "Kalau tanah sudah diwakafkan, bisa ditarik lagi nggak?",
    "Bedanya wakaf produktif sama wakaf biasa apa?",
    "Uang wakaf saya nanti dibagikan langsung ke fakir miskin atau gimana?",
    "Nazhir boleh nggak menginvestasikan dana wakaf ke properti komersial?",
]


def clean_content(content: str) -> str:
    if content.startswith("passage: "):
        return content[len("passage: "):]
    return content


def first_sentence(text: str, max_len: int = 200) -> str:
    text = text.strip()
    for sep in [". ", ".\n", "!", "?"]:
        idx = text.find(sep)
        if 0 < idx < max_len:
            return text[:idx + 1].strip()
    return (text[:max_len].strip() + "...") if len(text) > max_len else text


def format_doc_label(doc) -> str:
    source = doc.metadata.get("sumber") or doc.metadata.get("source", "Tidak Diketahui")
    page = doc.metadata.get("halaman") or doc.metadata.get("page", "-")
    return f"{source}, Hal. {page}"


def render_question_block(idx: int, question: str, res: dict) -> str:
    lines = [f"## {idx}. {question}", "", res["answer"].strip(), ""]

    docs = res.get("reranked_docs") or []
    lines.append("**Dokumen rujukan (top-3, dengan skor rerank):**")
    if docs:
        for doc in docs:
            score = doc.metadata.get("rerank_score", 0.0)
            content = clean_content(doc.page_content)
            lines.append(f"- [{format_doc_label(doc)}] (Rerank Score: {score:.4f}) {first_sentence(content)}")
    else:
        lines.append("- (tidak ada dokumen ditemukan)")
    lines.append("")
    lines.append("---")
    return "\n".join(lines)


def main():
    load_dotenv()

    print("[INFO] Memuat WaqfRAGPipeline (embedding model + FAISS index + reranker)...")
    pipeline = WaqfRAGPipeline()
    print("[SUCCESS] Pipeline siap.\n")

    blocks = [
        "# Hasil Tanya Jawab - WaqfRAG Chatbot",
        "",
        f"Model LLM: `{LLM_GEMINI_NAME}` (model_choice=\"{MODEL_CHOICE}\")  ",
        f"Skenario: RAG + Rerank (top-10 retrieval -> top-3 rerank)  ",
        "",
        "---",
    ]

    for i, question in enumerate(QUESTIONS, start=1):
        print(f"[{i}/{len(QUESTIONS)}] Memproses: '{question}'")
        try:
            res = pipeline.query(question, model_choice=MODEL_CHOICE, use_retrieval=USE_RETRIEVAL, use_rerank=USE_RERANK)
        except Exception as e:
            print(f"  [ERROR] Gagal: {e}")
            res = {"answer": f"[ERROR] Gagal menjalankan query: {e}", "reranked_docs": []}

        blocks.append(render_question_block(i, question, res))

        if i < len(QUESTIONS):
            time.sleep(DELAY_BETWEEN_CALLS_SEC)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks) + "\n")

    print(f"\n[SUCCESS] Selesai. Hasil {len(QUESTIONS)} pertanyaan tersimpan di: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
