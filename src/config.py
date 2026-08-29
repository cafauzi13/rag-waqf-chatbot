import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# ---------------------------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"             # Regulasi JDIH, Fatwa DSN-MUI, Korpus BWI (PDF)
PROCESSED_DATA_DIR = DATA_DIR / "processed" # Chunks & metadata
FAISS_INDEX_DIR = BASE_DIR / "faiss_index"  # Vector database FAISS lokal
RESULTS_DIR = BASE_DIR / "results"          # Output RAGAS & 60 respons Blinded Eval

FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# API Keys (Gemini 3.6 Flash & GPT-4o Mini)
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------------------------------------------------------------------
# Model Configurations (Sesuai Proposal)
# ---------------------------------------------------------------------------
# Embedding Model (Sub-bab 3.1.4)
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-base"

# Re-ranker Model (Sub-bab 3.1.6 & Abstrak)
RERANKER_MODEL_NAME = "mixedbread-ai/mxbai-rerank-base-v2"

# LLM Generator Models (Sub-bab 3.1.6 & Abstrak)
LLM_GEMINI_NAME = "gemini-3.6-flash"
LLM_OPENAI_NAME = "gpt-4o-mini"

# Parameter Generasi (Sub-bab 3.1.6)
TEMPERATURE = 0.0  # Bernilai 0 agar respons deterministik

# ---------------------------------------------------------------------------
# RAG Hyperparameters (Sesuai Proposal)
# ---------------------------------------------------------------------------
# Parameter Chunking (Sub-bab 3.1.4 - Baseline Zega 2025)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 80

# Parameter Retrieval & Re-ranking (Sub-bab 3.1.6)
TOP_K_RETRIEVAL = 20  # Retrieval FAISS awal (top-20)
TOP_K_RERANK = 3      # Penyaringan Re-ranker (top-3)

# Parameter Evaluasi (Sub-bab 3.1.5 & 3.1.7)
TOTAL_RAGAS_QUERIES = 30  # 20-30 skenario kueri
TOTAL_HUMAN_QUERIES = 10  # 10 skenario subset untuk human eval
