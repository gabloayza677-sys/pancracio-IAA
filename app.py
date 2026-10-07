import os
import streamlit as st
from groq import Groq

# -------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Pancracio IA | Futura Edition",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Tema Oscuro con Acentos Rojo Neón)
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* Importar fuente futurista */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Inter:wght@300;400;600&display=swap');

    /* Fondo principal y tipografía general */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #1a080c 0%, #08090c 70%, #030406 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Barra lateral en tono oscuro profundo */
    section[data-testid="stSidebar"] {
        background-color: rgba(12, 13, 18, 0.85) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 42, 95, 0.2);
    }

    /* Encabezados y títulos con estilo neón */
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff2a5f 0%, #ff5252 50%, #ff7b00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255, 42, 95, 0.3);
        margin-bottom: 0.1rem;
        letter-spacing: 1px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    /* Tarjeta de estado / estadísticas estilo "Futura 01" */
    .futura-card {
        background: rgba(20, 22, 31, 0.6);
        border: 1px solid rgba(255, 42, 95, 0.3);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), 0 0 15px rgba(255, 42, 95, 0.15);
        margin-bottom: 1.5rem;
    }

    .futura-badge {
        background: linear-gradient(90deg, #ff2a5f, #ff5252);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Botones primarios con degradado rojo */
    .stButton > button {
        background: linear-gradient(90deg, #ff2a5f 0%, #d90429 100%);
        color: #ffffff;
        border: 1px solid #ff5252;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 15px rgba(255, 42, 95, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(255, 42, 95, 0.8);
        border-color: #ffffff;
    }

    /* Contenedor y mensajes del Chat */
    .stChatMessage {
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    /* Mensaje del usuario */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255, 42, 95, 0.08);
        border: 1px solid rgba(255, 42, 95, 0.25);
    }

    /* Mensaje del asistente */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(18, 22, 33, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Input de chat estilizado */
    .stChatInput input {
        border: 1px solid rgba(255, 42, 95, 0.4) !important;
        background-color: rgba(12, 13, 18, 0.9) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }

    .stChatInput input:focus {
        border-color: #ff2a5f !important;
        box-shadow: 0 0 10px rgba(255, 42, 95, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# CLIENTE GROQ Y SECRETS
# -------------------------------------------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=groq_api_key)

# -------------------------------------------------------------------
# ESTADO DE LA SESIÓN (Múltiples chats)
# -------------------------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Desafío 01": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Desafío 01"

# -------------------------------------------------------------------
# BARRA LATERAL (Sidebar)
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#ff2a5f; font-family:Orbitron;'>🔴 PANCRACIO IA</h2>", unsafe_allow_html=True)
    st.caption("Módulo Avanzado de Inteligencia Artificial")
    
    st.markdown("---")
    
    if st.button("➕ Crear Nueva Sala", use_container_width=True):
        new_chat_num = len(st.session_state.chats) + 1
        new_chat_name = f"Desafío 0{new_chat_num}" if new_chat_num < 10 else f"Desafío {new_chat_num}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.active_chat = new_chat_name
        st.rerun()

    st.markdown("<h4 style='margin-top:1.5rem;'>💬 Conversaciones</h4>", unsafe_allow_html=True)
    
    chat_list = list(st.session_state.chats.keys())
    selected_chat = st.radio(
        "Salas activas:",
        options=chat_list,
        index=chat_list.index(st.session_state.active_chat),
        label_visibility="collapsed"
    )
    st.session_state.active_chat = selected_chat

    st.markdown("---")
    
    st.markdown("#### 📁 Adjuntar Archivo")
    uploaded_file = st.file_uploader(
        "Sube documentos de código o texto (.txt, .py, .md)",
        type=["txt", "py", "md"],
        label_visibility="collapsed"
    )
    
    file_text_content = ""
    if uploaded_file:
        try:
            file_text_content = uploaded_file.getvalue().decode("utf-8")
            st.success(f"📄 {uploaded_file.name} listo")
        except Exception:
            st.error("Error al procesar el archivo.")

# -------------------------------------------------------------------
# ÁREA PRINCIPAL DE LA PÁGINA
# -------------------------------------------------------------------
st.markdown('<h1 class="hero-title">PANCRACIO IA</h1>', unsafe_allow_html=True)

# Tarjeta de estado
st.markdown(f'''
<div class="futura-card">
    <span class="futura-badge">SISTEMA ACTIVO</span>
    <h3 style="margin-top: 0.5rem; margin-bottom: 0.2rem; color: #f8fafc;">Sala: {st.session_state.active_chat}</h3>
    <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">Modelo cargado: <b>openai/gpt-oss-20b</b> • Diseñado para resolución de desafíos y análisis de datos.</p>
</div>
''', unsafe_allow_html=True)

current_messages = st.session_state.chats[st.session_state.active_chat]

# Mostrar historial de mensajes
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("Escribe tu consulta o desafío..."):
    
    full_prompt = prompt
    if file_text_content:
        full_prompt += f"\n\n[Contenido del archivo {uploaded_file.name}]:\n{file_text_content}"

    user_msg = {"role": "user", "content": full_prompt}
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if file_text_content:
            st.info(f"📁 Documento adjunto procesado: {uploaded_file.name}")

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        api_messages = [{"role": m["role"], "content": m["content"]} for m in current_messages]
        
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=api_messages,
                stream=True,
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            current_messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")
