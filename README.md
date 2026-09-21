# 🕌 ZiswafRAG Chatbot - Asisten AI Regulasi & Literasi Wakaf, Zakat, dan Kurban

Sistem chatbot berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk menjawab pertanyaan seputar regulasi perwakafan, zakat-infak-sedekah, dan kurban di Indonesia — fatwa MUI/DSN-MUI, peraturan pemerintah/kementerian/BWI/BAZNAS, serta literasi dari masing-masing bidang.

---

## 📌 Arsitektur & Teknologi

* **Embedding Model**: `intfloat/multilingual-e5-base` (768 dimensi, Cosine Similarity dengan normalisasi vektor, prefiks asimetris `passage:`/`query:`)
* **Vector Store**: FAISS (Facebook AI Similarity Search) lokal
* **Re-ranker**: `mixedbread-ai/mxbai-rerank-base-v2` (Cross-Encoder)
* **LLM Generators**:
  * **Google Gemini 3.6 Flash** (Default - Dukungan Free Tier via Google AI Studio)
  * **OpenAI GPT-4o Mini** (Opsional)
  * **Llama 3.2 via Ollama** (Opsional, lokal, tanpa API key)
* **Framework RAG**: LangChain & HuggingFace Transformers
* **Ekstraksi PDF**: pdfplumber (layout-aware), fallback PyMuPDF
* **Evaluasi**: Ragas Framework (*Faithfulness, Answer Relevancy, Context Precision, Context Recall*)
* **Interfaces**: Terminal CLI (`cli_chat.py`) & Web UI (`app.py` via Streamlit)
* **Konfigurasi**: `config.yaml` (satu sumber kebenaran untuk seluruh hyperparameter pipeline)

Alasan pemilihan tiap tools ada di bagian [Kenapa Tools Ini?](#-kenapa-tools-ini) di bawah.

---

## 📂 Struktur Direktori

```text
rag-waqf-chatbot/
│
├── data/
│   ├── raw/
│   │   ├── wakaf/{regulasi,literasi}/               # PDF regulasi & literasi wakaf
│   │   ├── zakat-infak-sedekah/{regulasi,literasi}/ # PDF regulasi & literasi zakat/infak/sedekah
│   │   └── kurban/{regulasi,literasi}/              # PDF regulasi & literasi kurban
│   ├── processed/
│   │   └── chunks.jsonl       # Checkpoint chunk siap-index (teks + metadata), dari src/ingest.py
│   └── evaluation_set.json    # Skenario kueri benchmark & ground truth
│
├── faiss_index/                # Database vektor FAISS (dibuat via src/build_index.py)
├── results/                    # Output evaluasi, benchmark, & cleaning_debug
│   └── cleaning_debug/         # Dump teks bersih + statistik per dokumen (verifikasi manual)
│
├── config.yaml                 # SUMBER KEBENARAN seluruh hyperparameter pipeline
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Thin-loader config.yaml + path & API key dari .env
│   ├── cleaning.py             # Fungsi cleaning teks PDF (header/footer, dehyphenation, dst)
│   ├── metadata.py             # Turunkan kategori/jenis/sumber dari struktur folder
│   ├── segmentation.py         # Pecah teks per Pasal/diktum (regulasi) atau BAB/heading (literasi)
│   ├── chunking.py             # Chunking di dalam tiap segmen + prefiks E5 "passage: "
│   ├── ingest.py               # Tahap 1: PDF -> data/processed/chunks.jsonl
│   ├── build_index.py          # Tahap 2: chunks.jsonl -> embedding -> FAISS
│   ├── inspect_faiss.py        # Debugging & audit isi index FAISS
│   ├── reranker.py             # Modul Cross-Encoder Reranker
│   ├── pipeline.py             # Core RAG Pipeline (Retrieve -> Rerank -> LLM)
│   └── evaluator.py            # Modul evaluasi Ragas & Blinded Evaluation
│
├── scripts/
│   ├── verify_cleaning.py            # Dump hasil cleaning tiap PDF untuk review manual
│   ├── generate_rename_inventory.py  # Draft usulan penamaan ulang PDF (xlsx, read-only)
│   ├── apply_rename_inventory.py     # Eksekusi rename fisik dari inventaris yang sudah direview
│   ├── compare_scenarios.py          # Perbandingan manual 3 skenario RAG
│   └── run_qa_batch.py               # Jalankan daftar pertanyaan tetap, simpan ke markdown
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

# Buat virtual environment (Python 3.11 direkomendasikan)
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

### 3. Konfigurasi Pipeline
Seluruh hyperparameter (model embedding/reranker/generator, ukuran chunk, top-k retrieval/rerank, ambang cleaning, dsb) ada di **`config.yaml`** di root proyek. Ubah file ini kalau perlu tuning — kode tidak butuh diubah untuk ganti angka/model.

### 4. Pembuatan Database Vektor (Data Ingestion)

Dipecah jadi 2 tahap supaya ganti model embedding tidak perlu ekstraksi PDF ulang dari nol:

```bash
# Tahap 1: PDF di data/raw/ -> data/processed/chunks.jsonl (murah, tanpa GPU)
python -m src.ingest

# Tahap 2: chunks.jsonl -> embedding -> faiss_index/ (lebih mahal)
python -m src.build_index
```

Jalankan ulang Tahap 1 kalau ada dokumen PDF baru/berubah di `data/raw/`. Kalau cuma ganti model embedding di `config.yaml`, cukup jalankan ulang Tahap 2 saja (chunks.jsonl sudah tersedia).

Untuk menambah domain baru (mis. `data/raw/<domain-baru>/{regulasi,literasi}/`), tidak perlu ubah kode — struktur folder otomatis terbaca sebagai kategori baru.

---

## 💬 Menjalankan Chatbot

### A. Melalui Terminal / Console (CLI)
Sangat cocok untuk pengujian backend tanpa browser:
```bash
python cli_chat.py
```
* Fitur: Memilih model (Gemini / OpenAI / Ollama / Bandingkan Gemini & OpenAI), memilih skenario RAG (LLM saja / RAG tanpa rerank / RAG + rerank), dan melihat **RAG Trace** (dokumen rujukan & skor relevansi).

### B. Melalui Antarmuka Web (Streamlit)
```bash
streamlit run app.py
```
* Buka browser di `http://localhost:8501`.

---

## 📊 Menjalankan Benchmark & Evaluasi Ragas

Untuk menjalankan evaluasi skenario kueri dan menguji metrik otomatis (*Ragas*):
```bash
python run_benchmark.py
```
Hasil evaluasi akan disimpan di folder `results/`:
* `blinded_evaluation_responses.csv`: respons dari kedua model.
* `ragas_summary.json`: Ringkasan metrik evaluasi Ragas.

Untuk verifikasi manual kualitas cleaning PDF, atau mengecek/menyusun ulang penamaan file korpus:
```bash
python scripts/verify_cleaning.py             # dump hasil cleaning ke results/cleaning_debug/
python scripts/generate_rename_inventory.py   # draft usulan rename (xlsx, read-only)
python scripts/apply_rename_inventory.py      # eksekusi rename setelah inventaris direview
```

---

## 🔌 Integrasi ke Backend / Fitur API (Contoh FastAPI / Flask)

Bagi tim pengembang yang ingin mengintegrasikan pipeline RAG ini sebagai fitur API atau service backend:

```python
from src.pipeline import WaqfRAGPipeline

# Inisialisasi pipeline (cukup sekali saat server startup)
pipeline = WaqfRAGPipeline()

# Menjalankan kueri (use_retrieval/use_rerank default dari config.yaml,
# bisa di-override per panggilan untuk kebutuhan evaluasi/perbandingan skenario)
user_question = "Apa saja syarat pendaftaran nazhir wakaf uang?"
result = pipeline.query(user_question, model_choice="gemini")

# Mengambil jawaban dan dokumen pendukung
answer = result["answer"]
source_docs = result["reranked_docs"]

print("Jawaban:", answer)
for doc in source_docs:
    print(f"Sumber: {doc.metadata['sumber']} ({doc.metadata['unit']}, Hal. {doc.metadata['halaman']})")
```

---

## 🧩 Kenapa Tools Ini?

| Tool | Peran | Alasan |
|---|---|---|
| `intfloat/multilingual-e5-base` | Embedding (768 dim) | Dukung Bahasa Indonesia, desain query/passage asimetris cocok untuk retrieval, skor kuat di benchmark multibahasa (MIRACL), ringan jalan tanpa GPU wajib. |
| `mixedbread-ai/mxbai-rerank-base-v2` | Reranker | Cross-encoder baca query+dokumen bersamaan → lebih presisi dari bi-encoder untuk menyaring top-3 dari top-10. |
| FAISS | Vector store | Lokal, gratis, cukup cepat untuk skala ribuan chunk tanpa perlu server database eksternal. |
| pdfplumber (+ fallback PyMuPDF) | Ekstraksi PDF | Layout-aware — dibutuhkan untuk deteksi header/footer berbasis posisi baris, bukan cuma dump teks polos; PyMuPDF sebagai fallback lebih toleran & dipakai render PNG debug. |
| LangChain | Orkestrasi | Satu interface yang sama untuk Gemini/OpenAI/Ollama tanpa tulis client API terpisah per provider. |
| `RecursiveCharacterTextSplitter` | Chunking dalam segmen | Memotong berdasar hierarki pemisah (paragraf→baris→kata), bukan potong buta per-N-karakter. |
| Regex penanda struktur (custom) | Segmentasi Pasal/BAB | Dokumen hukum Indonesia punya penanda sangat teratur (Pasal N, BAB, diktum) — presisi & deterministik tanpa model NLP tambahan. |
| Ragas | Evaluasi | Framework standar RAG untuk metrik Faithfulness/Answer Relevancy/Context Precision/Recall sesuai metodologi skripsi. |
| Streamlit | Web UI | Prototyping cepat, cocok untuk skala demo/skripsi/pilot kecil. |
