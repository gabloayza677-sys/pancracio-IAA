import os
import streamlit as st
from groq import Groq

# -------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Pancracio IA",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Inspirados en la interfaz de Gemini)
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo oscuro con resplandor central azul/rojo */
    .stApp {
        background: radial-gradient(circle at 50% 45%, #18101a 0%, #0d0e12 60%, #050507 100%);
        color: #e2e8f0;
    }

    /* Ocultar elementos predeterminados innecesarios */
    #MainMenu, header, footer {visibility: hidden;}

    /* Contenedor central principal */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 5vh;
        margin-bottom: 2rem;
    }

    /* Título estilo Gemini */
    .gemini-title {
        font-size: 2.8rem;
        font-weight: 500;
        color: #f1f5f9;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }

    /* Barra lateral estilo Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 14, 18, 0.9) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Botón flotante para cambiar de chat */
    .stButton > button {
        background: linear-gradient(90deg, #e11d48 0%, #be123c 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
    }

    /* Estilo para las tarjetas de chat */
    .stChatMessage {
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }

    /* Mensaje del usuario */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Mensaje de la IA */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(225, 29, 72, 0.06);
        border: 1px solid rgba(225, 29, 72, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# CLIENTE DE GROQ
# -------------------------------------------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró la variable GROQ_API_KEY en los Secrets.")
    st.stop()

client = Groq(api_key=groq_api_key)

# -------------------------------------------------------------------
# DICCIONARIO DE MODELOS CON NOMBRES LLAMATIVOS
# -------------------------------------------------------------------
MODELOS_DISPONIBLES = {
    "⚡ Pancracio Flash (Ultra Rápido)": "openai/gpt-oss-20b",
    "🧠 Pancracio Pro (Razonamiento Complejo)": "openai/gpt-oss-20b",
    "🎨 Pancracio Creativo (Textos e Ideas)": "openai/gpt-oss-20b"
}

# -------------------------------------------------------------------
# GESTIÓN DE SESIÓN
# -------------------------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Nuevo Chat": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Nuevo Chat"

# -------------------------------------------------------------------
# BARRA LATERAL (Menú de salas y archivos)
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🤖 **Pancracio Studio**")
    st.caption("Interfaz Minimalista")
    st.markdown("---")
    
    if st.button("➕ Nuevo Chat", use_container_width=True):
        num = len(st.session_state.chats) + 1
        name = f"Chat {num}"
        st.session_state.chats[name] = []
        st.session_state.active_chat = name
        st.rerun()

    st.markdown("#### 💬 Conversaciones")
    chat_list = list(st.session_state.chats.keys())
    selected_chat = st.radio(
        "Salas",
        options=chat_list,
        index=chat_list.index(st.session_state.active_chat),
        label_visibility="collapsed"
    )
    st.session_state.active_chat = selected_chat

    st.markdown("---")
    st.markdown("#### 📁 Adjuntar Texto/Código")
    uploaded_file = st.file_uploader(
        "Cargar archivo (.txt, .py, .md)",
        type=["txt", "py", "md"],
        label_visibility="collapsed"
    )
    
    file_text = ""
    if uploaded_file:
        try:
            file_text = uploaded_file.getvalue().decode("utf-8")
            st.success(f"📎 {uploaded_file.name} cargado")
        except Exception:
            st.error("Error al leer el archivo.")
