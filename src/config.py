import os
from pathlib import Path

import yaml
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
CONFIG_YAML_PATH = BASE_DIR / "config.yaml"

FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# API Keys (Gemini & OpenAI) -- tetap dari .env, BUKAN config.yaml (secret,
# bukan hyperparameter, dan config.yaml akan dibekukan/dicek ke git)
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM Lokal via Ollama (untuk uji coba lokal tanpa API key) -- opsi tambahan
# di luar 2 generator yang dievaluasi Ragas, tetap dari env var.
LLM_OLLAMA_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ---------------------------------------------------------------------------
# config.yaml -- SUMBER KEBENARAN untuk seluruh hyperparameter pipeline.
# Konstanta di bawah ini dipertahankan namanya untuk kompatibilitas mundur
# dengan kode yang sudah ada (mis. `from src.config import CHUNK_SIZE`),
# tapi nilainya sekarang berasal dari config.yaml, bukan hardcoded di sini.
# ---------------------------------------------------------------------------
with open(CONFIG_YAML_PATH, "r", encoding="utf-8") as _f:
    _CFG = yaml.safe_load(_f)

EMBEDDING_MODEL_NAME = _CFG["embedding_model"]
RERANKER_MODEL_NAME = _CFG["rerank_model"]

GENERATOR = _CFG["generator"]
# LLM_GEMINI_NAME/LLM_OPENAI_NAME dipertahankan sebagai nama terpisah
# (dipakai pipeline.py untuk kedua generator sekaligus, bukan cuma yang
# jadi default di config.yaml).
LLM_GEMINI_NAME = "gemini-3.6-flash"
LLM_OPENAI_NAME = "gpt-4o-mini"

TEMPERATURE = float(_CFG["temperature"])

CHUNK_SIZE = int(_CFG["chunk_size"])
CHUNK_OVERLAP = int(_CFG["chunk_overlap"])

USE_RETRIEVAL = bool(_CFG["use_retrieval"])
TOP_K_RETRIEVAL = int(_CFG["top_k_retrieval"])
USE_RERANK = bool(_CFG["use_rerank"])
TOP_K_RERANK = int(_CFG["top_k_rerank"])

HEADER_FOOTER_THRESHOLD = float(_CFG["header_footer_threshold"])
HEADER_FOOTER_WINDOW_LINES = int(_CFG["header_footer_window_lines"])
MIN_PAGES_FOR_HEADER_FOOTER_DETECTION = int(_CFG["min_pages_for_header_footer_detection"])
MIN_PAGE_CHARS = int(_CFG["min_page_chars"])
DOT_LEADER_RATIO_THRESHOLD = float(_CFG["dot_leader_ratio_threshold"])
BLANK_UNDERSCORE_RATIO_THRESHOLD = float(_CFG["blank_underscore_ratio_threshold"])

# ---------------------------------------------------------------------------
# Parameter Evaluasi (Sub-bab 3.1.5 & 3.1.7) -- bukan hyperparameter
# pipeline, tetap konstanta Python biasa.
# ---------------------------------------------------------------------------
TOTAL_RAGAS_QUERIES = 30  # 20-30 skenario kueri
TOTAL_HUMAN_QUERIES = 10  # 10 skenario subset untuk human eval
