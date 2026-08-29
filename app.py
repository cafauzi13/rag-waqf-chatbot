import os
import streamlit as st
from src.pipeline import WaqfRAGPipeline
from langchain_core.documents import Document

# 1. Konfigurasi Halaman Streamlit (Tema Gelap dan Lebar)
st.set_page_config(
    page_title="WaqfRAG Chatbot - Wakaf Produktif & Regulasi",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injeksi CSS Kustom untuk Tampilan Premium
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Font Global */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Judul Utama */
    .main-title {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 5px;
        text-align: left;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 25px;
        font-weight: 400;
    }
    
    /* Desain Card Dokumen */
    .doc-card {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 12px 15px;
        margin-bottom: 10px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .doc-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .doc-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #34d399;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .doc-content {
        font-size: 0.9rem;
        color: #e5e7eb;
        line-height: 1.5;
    }
    .score-badge {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 600;
    }
    .score-faiss {
        background-color: #3b82f6;
        color: white;
    }
    .score-rerank {
        background-color: #10b981;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Inisialisasi State Aplikasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Memuat pipeline RAG (caching agar tidak reload model embedding tiap refresh)
@st.cache_resource
def get_rag_pipeline():
    try:
        return WaqfRAGPipeline()
    except Exception as e:
        st.error(f"Gagal menginisialisasi RAG Pipeline: {e}")
        return None

pipeline = get_rag_pipeline()

# 4. Sidebar Konfigurasi (Sidebar Kiri)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/mosque.png", width=80)
    st.markdown("### ⚙️ Konfigurasi RAG Chatbot")
    
    # Pilihan Model LLM
    model_option = st.selectbox(
        "Pilih Generator LLM:",
        ["Gemini 3.6 Flash", "GPT-4o Mini"],
        index=0,
        help="Gemini 3.6 Flash dan GPT-4o Mini akan dibandingkan sesuai proposal penelitian."
    )
    model_choice = "gemini" if "Gemini" in model_option else "openai"
    
    st.markdown("---")
    
    # Input API Key jika belum diset di .env
    st.markdown("### 🔑 API Credentials")
    
    # Gemini API Key
    gemini_key_env = os.getenv("GEMINI_API_KEY")
    if not gemini_key_env:
        gemini_key_input = st.text_input(
            "Gemini API Key:",
            type="password",
            placeholder="Masukkan GEMINI_API_KEY..."
        )
        if gemini_key_input:
            os.environ["GEMINI_API_KEY"] = gemini_key_input
    else:
        st.success("✅ GEMINI_API_KEY terdeteksi di .env")
        
    # OpenAI API Key
    openai_key_env = os.getenv("OPENAI_API_KEY")
    if not openai_key_env:
        openai_key_input = st.text_input(
            "OpenAI API Key:",
            type="password",
            placeholder="Masukkan OPENAI_API_KEY..."
        )
        if openai_key_input:
            os.environ["OPENAI_API_KEY"] = openai_key_input
    else:
        st.success("✅ OPENAI_API_KEY terdeteksi di .env")

    st.markdown("---")
    st.markdown(
        """
        ### 📊 RAG Parameters:
        - **Embedding**: `multilingual-e5-base`
        - **Reranker**: `mxbai-rerank-base-v2`
        - **FAISS Top-K**: 10 Chunks
        - **Reranked Top-K**: 3 Chunks
        - **Chunk Size / Overlap**: 800 / 80
        """
    )

# 5. Header Panel Utama
st.markdown("<h1 class='main-title'>🕌 WaqfRAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Asisten AI Pintar Regulasi Wakaf & Panduan Literasi Wakaf Produktif BWI</div>", unsafe_allow_html=True)

# Peringatan jika API Key belum siap
if model_choice == "gemini" and not os.getenv("GEMINI_API_KEY"):
    st.warning("⚠️ GEMINI_API_KEY belum terdeteksi. Silakan masukkan di sidebar atau buat file .env.")
elif model_choice == "openai" and not os.getenv("OPENAI_API_KEY"):
    st.warning("⚠️ OPENAI_API_KEY belum terdeteksi. Silakan masukkan di sidebar atau buat file .env.")

# 6. Menampilkan Riwayat Obrolan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Jika ada dokumen pendukung dalam riwayat, tampilkan kembali detailnya
        if "retrieved_docs" in message and "reranked_docs" in message:
            with st.expander("🔍 Detail Analisis Penelusuran Dokumen (RAG Trace)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### 🎯 Top-3 Reranked Chunks (Cross-Encoder)")
                    for doc in message["reranked_docs"]:
                        source = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "-")
                        score = doc.metadata.get("rerank_score", 0.0)
                        content = doc.page_content[len("passage: "):] if doc.page_content.startswith("passage: ") else doc.page_content
                        st.markdown(
                            f"""
                            <div class='doc-card'>
                                <div class='doc-header'>
                                    <span>📄 {source} (Hal. {page})</span>
                                    <span class='score-badge score-rerank'>Rerank: {score:.4f}</span>
                                </div>
                                <div class='doc-content'>{content[:200]}...</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                with col2:
                    st.markdown("##### ⚡ Top-10 FAISS Retrieval Chunks")
                    for doc in message["retrieved_docs"]:
                        source = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "-")
                        score = doc.metadata.get("similarity_score", 0.0)
                        content = doc.page_content[len("passage: "):] if doc.page_content.startswith("passage: ") else doc.page_content
                        st.markdown(
                            f"""
                            <div class='doc-card' style='border-left: 4px solid #3b82f6;'>
                                <div class='doc-header'>
                                    <span>📄 {source} (Hal. {page})</span>
                                    <span class='score-badge score-faiss'>Dist L2: {score:.4f}</span>
                                </div>
                                <div class='doc-content'>{content[:150]}...</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# 7. Penerimaan Kueri Baru dari User
if user_query := st.chat_input("Tanyakan tentang regulasi wakaf uang, pendaftaran nazhir, ruislag, dll..."):
    
    # Tampilkan pesan user ke chat
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Jalankan kueri ke pipeline RAG
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("⏳ *Sedang mencari dokumen dan merumuskan jawaban...*")
        
        if not pipeline:
            answer = "Gagal memproses kueri karena pipeline RAG tidak terinisialisasi."
            retrieved_docs = []
            reranked_docs = []
        else:
            # Query pipeline
            res = pipeline.query(user_query, model_choice=model_choice)
            answer = res["answer"]
            retrieved_docs = res["retrieved_docs"]
            reranked_docs = res["reranked_docs"]
            
        # Update respons asisten ke chat
        response_placeholder.markdown(answer)
        
        # Simpan pesan asisten beserta metadata dokumen untuk riwayat
        message_data = {
            "role": "assistant",
            "content": answer,
            "retrieved_docs": retrieved_docs,
            "reranked_docs": reranked_docs
        }
        st.session_state.messages.append(message_data)
        
        # Tampilkan Detail Analisis Dokumen Pendukung secara interaktif
        if reranked_docs:
            with st.expander("🔍 Detail Analisis Penelusuran Dokumen (RAG Trace)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### 🎯 Top-3 Reranked Chunks (Cross-Encoder)")
                    for doc in reranked_docs:
                        source = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "-")
                        score = doc.metadata.get("rerank_score", 0.0)
                        content = doc.page_content[len("passage: "):] if doc.page_content.startswith("passage: ") else doc.page_content
                        st.markdown(
                            f"""
                            <div class='doc-card'>
                                <div class='doc-header'>
                                    <span>📄 {source} (Hal. {page})</span>
                                    <span class='score-badge score-rerank'>Rerank: {score:.4f}</span>
                                </div>
                                <div class='doc-content'>{content[:250]}...</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                with col2:
                    st.markdown("##### ⚡ Top-10 FAISS Retrieval Chunks")
                    for doc in retrieved_docs:
                        source = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "-")
                        score = doc.metadata.get("similarity_score", 0.0)
                        content = doc.page_content[len("passage: "):] if doc.page_content.startswith("passage: ") else doc.page_content
                        st.markdown(
                            f"""
                            <div class='doc-card' style='border-left: 4px solid #3b82f6;'>
                                <div class='doc-header'>
                                    <span>📄 {source} (Hal. {page})</span>
                                    <span class='score-badge score-faiss'>Dist L2: {score:.4f}</span>
                                </div>
                                <div class='doc-content'>{content[:150]}...</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
