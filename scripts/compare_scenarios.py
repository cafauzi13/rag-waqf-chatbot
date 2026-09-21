"""
scripts/compare_scenarios.py

Script perbandingan MANUAL 3 skenario RAG (LLM Saja / RAG tanpa Rerank /
RAG + Rerank) untuk 6 pertanyaan uji yang mewakili berbagai jenis kasus:
pertanyaan dasar, sintesis multi-dokumen, out-of-domain, istilah mirip,
sintesis sejarah, dan syarat yang rawan tertukar.

PENTING: ini BUKAN evaluasi otomatis (tidak memakai Ragas atau metrik apa
pun). Script ini hanya menjalankan pipeline.query() untuk tiap kombinasi
pertanyaan x skenario, lalu menyimpan jawaban & dokumen pendukungnya apa
adanya ke file markdown -- tidak ada kesimpulan/analisis otomatis di sini.
Penilaian akurasi, risiko halusinasi, dan kesalahan konsep dilakukan
manual oleh peneliti dengan membaca file hasilnya.

Script ini memanggil WaqfRAGPipeline.query() dengan parameter
`use_retrieval`/`use_rerank` (Kiriman B menggantikan parameter `scenario`
string yang lama).
"""

import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Memastikan root direktori proyek ada di sys.path (script ini ada di
# scripts/, satu level di bawah root -- pola yang sama seperti cli_chat.py)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.pipeline import WaqfRAGPipeline
from src.config import RESULTS_DIR, LLM_GEMINI_NAME

MODEL_CHOICE = "gemini"
# (label, use_retrieval, use_rerank) -- menggantikan string "scenario" lama.
SCENARIOS = [
    ("llm_only", False, False),
    ("rag_no_rerank", True, False),
    ("rag_rerank", True, True),
]
OUTPUT_PATH = RESULTS_DIR / "scenario_comparison.md"

# Jeda antar pemanggilan LLM untuk menghindari rate limit API Gemini Free Tier
# (pola yang sama seperti di src/evaluator.py).
DELAY_BETWEEN_CALLS_SEC = 4

# 6 pertanyaan uji, masing-masing mewakili satu jenis kasus (lihat komentar
# di tiap baris untuk alasan pemilihannya).
TEST_QUESTIONS = [
    "Apa itu wakaf produktif?",                                   # pertanyaan dasar, jawaban eksplisit ada di 1 dokumen
    "Apa dasar hukum dan cara kerja wakaf uang di Indonesia?",     # butuh gabung info dari UU dan Fatwa DSN-MUI
    "Bagaimana hukum zakat fitrah?",                               # di luar domain wakaf, harus ditolak dengan jujur
    "Apa perbedaan wakaf produktif dengan wakaf konsumtif?",       # istilah mirip, rawan tertukar
    "Siapa saja sahabat Nabi yang mewakafkan hartanya?",           # butuh sintesis dari beberapa dokumen sejarah
    "Apa syarat menjadi Nazhir wakaf uang?",                       # rawan tertukar dengan syarat Waqif
]


def clean_content(content: str) -> str:
    """Hilangkan prefiks 'passage: ' dari isi dokumen (artefak preprocessing E5)."""
    if content.startswith("passage: "):
        return content[len("passage: "):]
    return content


def first_sentence(text: str, max_len: int = 200) -> str:
    """
    Ambil kira-kira 1 kalimat pertama dari isi dokumen, untuk daftar dokumen
    yang ringkas sesuai format yang diminta (bukan seluruh isi chunk).
    """
    text = text.strip()
    for sep in [". ", ".\n", "!", "?"]:
        idx = text.find(sep)
        if 0 < idx < max_len:
            return text[:idx + 1].strip()
    return (text[:max_len].strip() + "...") if len(text) > max_len else text


def format_doc_label(doc) -> str:
    source = doc.metadata.get("sumber") or doc.metadata.get("source", "Tidak Diketahui")
    page = doc.metadata.get("halaman") or doc.metadata.get("page", "-")
    unit = doc.metadata.get("unit")
    unit_info = f", {unit}" if unit else ""
    return f"{source}{unit_info}, Hal. {page}"


def render_question_block(question: str, res: dict) -> str:
    """
    Membangun satu blok markdown untuk satu pertanyaan, berisi hasil dari
    ketiga skenario, sesuai format persis yang diminta:
      ## Pertanyaan -> ### Skenario I/II/III -> daftar dokumen (untuk II & III)
    """
    llm_only = res["llm_only"]
    rag_no_rerank = res["rag_no_rerank"]
    rag_rerank = res["rag_rerank"]

    lines = []
    lines.append(f"## Pertanyaan: {question}")
    lines.append("")

    # --- Skenario I: tidak ada dokumen sama sekali (retrieved_docs/reranked_docs kosong) ---
    lines.append("### Skenario I - LLM Saja")
    lines.append(llm_only["answer"].strip())
    lines.append("")

    # --- Skenario II: dokumen dari retrieved_docs (top-10, BELUM di-rerank), tanpa skor ---
    lines.append("### Skenario II - RAG tanpa Rerank")
    lines.append(rag_no_rerank["answer"].strip())
    lines.append("Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):")
    docs_ii = rag_no_rerank.get("retrieved_docs") or []
    if docs_ii:
        for doc in docs_ii:
            content = clean_content(doc.page_content)
            lines.append(f"- [{format_doc_label(doc)}] {first_sentence(content)}")
    else:
        lines.append("- (tidak ada dokumen ditemukan)")
    lines.append("")

    # --- Skenario III: dokumen dari reranked_docs (top-3), dengan rerank_score ---
    lines.append("### Skenario III - RAG + Rerank")
    lines.append(rag_rerank["answer"].strip())
    lines.append("Dokumen yang dipakai (top-3, dengan skor rerank):")
    docs_iii = rag_rerank.get("reranked_docs") or []
    if docs_iii:
        for doc in docs_iii:
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
        "# Perbandingan Manual 3 Skenario RAG - WaqfRAG Chatbot",
        "",
        f"Model LLM: `{LLM_GEMINI_NAME}` (model_choice=\"{MODEL_CHOICE}\")  ",
        "Skenario: (I) LLM Saja | (II) RAG tanpa Rerank | (III) RAG + Rerank  ",
        "Catatan: hasil ini untuk dibaca & dinilai manual, bukan output evaluasi otomatis (Ragas).",
        "",
        "---",
    ]

    for i, question in enumerate(TEST_QUESTIONS, start=1):
        print(f"[{i}/{len(TEST_QUESTIONS)}] Memproses pertanyaan: '{question}'")

        results_per_scenario = {}
        for j, (label, use_retrieval, use_rerank) in enumerate(SCENARIOS):
            print(f"    - Menjalankan skenario '{label}'...")
            try:
                res = pipeline.query(question, model_choice=MODEL_CHOICE, use_retrieval=use_retrieval, use_rerank=use_rerank)
            except Exception as e:
                print(f"      [ERROR] Skenario '{label}' gagal: {e}")
                res = {"answer": f"[ERROR] Gagal menjalankan skenario: {e}", "retrieved_docs": [], "reranked_docs": []}
            results_per_scenario[label] = res

            # Jeda antar panggilan LLM (kecuali setelah panggilan terakhir) untuk
            # menghindari rate limit API Gemini Free Tier.
            is_last_call = (i == len(TEST_QUESTIONS)) and (j == len(SCENARIOS) - 1)
            if not is_last_call:
                time.sleep(DELAY_BETWEEN_CALLS_SEC)

        blocks.append(render_question_block(question, results_per_scenario))

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks) + "\n")

    print(f"\n[SUCCESS] Selesai. Hasil perbandingan {len(TEST_QUESTIONS)} pertanyaan x {len(SCENARIOS)} skenario tersimpan di: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
