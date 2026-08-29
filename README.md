# 🕌 WaqfRAG Chatbot - Asisten AI Regulasi & Literasi Wakaf Produktif

Sistem chatbot berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk menjawab pertanyaan seputar regulasi perwakafan di Indonesia, fatwa DSN-MUI, panduan pendaftaran nazhir, serta literasi wakaf produktif Badan Wakaf Indonesia (BWI).

---

## 📌 Arsitektur & Teknologi

* **Embedding Model**: `intfloat/multilingual-e5-base` (Cosine Similarity dengan normalisasi vektor)
* **Vector Store**: FAISS (Facebook AI Similarity Search) lokal
* **Re-ranker**: `mixedbread-ai/mxbai-rerank-base-v2` (Cross-Encoder)
* **LLM Generators**:
  * **Google Gemini 3.6 Flash** (Default - Dukungan Free Tier via Google AI Studio)
  * **OpenAI GPT-4o Mini** (Opsional)
* **Framework RAG**: LangChain & HuggingFace Transformers
* **Evaluasi**: Ragas Framework (*Faithfulness, Answer Relevancy, Context Precision, Context Recall*)
* **Interfaces**: Terminal CLI (`cli_chat.py`) & Web UI (`app.py` via Streamlit)

---

## 📂 Struktur Direktori

```text
rag-waqf-chatbot/
│
├── data/
│   ├── raw/
│   │   ├── bwi-literasi/      # 25 file PDF literasi BWI
│   │   └── regulasi/          # 25 file PDF UU & peraturan wakaf
│   ├── processed/             # Ekstraksi chunk CSV
│   └── evaluation_set.json    # 30 skenario kueri benchmark & ground truth
│
├── faiss_index/               # Database vektor FAISS (dibuat via ingest.py)
├── results/                   # Output file respons evaluasi & benchmark
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Parameter global & hyperparameter RAG
│   ├── ingest.py              # Ekstraksi, cleaning, chunking, & pembuatan FAISS
│   ├── inspect_faiss.py       # Debugging & audit chunks FAISS
│   ├── reranker.py            # Modul Cross-Encoder Reranker
│   ├── pipeline.py            # Core RAG Pipeline (Retrieve -> Rerank -> LLM)
│   └── evaluator.py           # Modul evaluasi Ragas & Blinded Evaluation
│
├── app.py                     # Antarmuka Web Streamlit
├── cli_chat.py                # Antarmuka Terminal Interaktif
├── run_benchmark.py           # Skrip eksekusi benchmark Ragas
├── requirements.txt           # Dependensi Python
├── .env.example               # Template environment variables
└── README.md
```

---

## 🚀 Panduan Instalasi & Penggunaan

### 1. Kloning Repositori & Setup Environment
```bash
# Clone repository
git clone <repository-url>
cd rag-waqf-chatbot

# Buat virtual environment
python -m venv .venv

# Aktivasi virtual environment
# Windows:
.venv\Scripts\activate
# Linux/MacOS:
source .venv/bin/activate

# Install dependensi
pip install -r requirements.txt
```

### 2. Konfigurasi API Key
Salin file `.env.example` menjadi `.env` lalu isi API key Anda:
```bash
cp .env.example .env
```
Buka file `.env` dan masukkan API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Opsional
```
*(Catatan: Kunci API Gemini bisa didapatkan gratis di [Google AI Studio](https://aistudio.google.com/)).*

### 3. Pembuatan Database Vektor (Data Ingestion)
Jika database FAISS belum dibuat atau terdapat dokumen PDF baru di `data/raw/`, jalankan:
```bash
python -m src.ingest
```

---

## 💬 Menjalankan Chatbot

### A. Melalui Terminal / Console (CLI)
Sangat cocok untuk pengujian backend tanpa browser:
```bash
python cli_chat.py
```
* Fitur: Memilih model (Gemini / OpenAI / Bandingkan Keduanya) dan melihat **RAG Trace** (Top-3 dokumen rujukan & skor relevansi).

### B. Melalui Antarmuka Web (Streamlit)
```bash
streamlit run app.py
```
* Buka browser di `http://localhost:8501`.

---

## 📊 Menjalankan Benchmark & Evaluasi Ragas

Untuk menjalankan evaluasi 30 skenario kueri dan menguji metrik otomatis (*Ragas*):
```bash
python run_benchmark.py
```
Hasil evaluasi akan disimpan di folder `results/`:
* `blinded_evaluation_responses.csv`: 60 respons dari kedua model.
* `ragas_summary.json`: Ringkasan metrik evaluasi Ragas.

---

## 🔌 Integrasi ke Backend / Fitur API (Contoh FastAPI / Flask)

Bagi tim pengembang yang ingin mengintegrasikan pipeline RAG ini sebagai fitur API atau service backend:

```python
from src.pipeline import WaqfRAGPipeline

# Inisialisasi pipeline (cukup sekali saat server startup)
pipeline = WaqfRAGPipeline()

# Menjalankan kueri
user_question = "Apa saja syarat pendaftaran nazhir wakaf uang?"
result = pipeline.query(user_question, model_choice="gemini")

# Mengambil jawaban dan dokumen pendukung
answer = result["answer"]
source_docs = result["reranked_docs"]

print("Jawaban:", answer)
for doc in source_docs:
    print(f"Sumber: {doc.metadata['source']} (Hal. {doc.metadata['page']})")
```
