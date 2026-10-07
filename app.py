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
# ESTILOS CSS PERSONALIZADOS
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo oscuro con degradado radial */
    .stApp {
        background: radial-gradient(circle at 50% 45%, #18101a 0%, #0d0e12 60%, #050507 100%);
        color: #e2e8f0;
    }

    /* Ocultar encabezados por defecto */
    #MainMenu, header, footer {visibility: hidden;}

    /* Título estilo Gemini */
    .gemini-title {
        font-size: 2.8rem;
        font-weight: 600;
        color: #f1f5f9;
        text-align: center;
        margin-top: 10vh;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 14, 18, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Botones */
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

    /* Contenedor de mensajes */
    .stChatMessage {
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(225, 29, 72, 0.08);
        border: 1px solid rgba(225, 29, 72, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# CONEXIÓN CON GROQ
# -------------------------------------------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró la variable GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=groq_api_key)

# Modelos disponibles
MODELOS_DISPONIBLES = {
    "⚡ Pancracio Flash (Ultra Rápido)": "openai/gpt-oss-20b",
    "🧠 Pancracio Pro (Razonamiento)": "openai/gpt-oss-20b",
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
# BARRA LATERAL
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🤖 **Pancracio Studio**")
    st.caption("Modo Minimalista")
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
    st.markdown("#### 📁 Adjuntar Archivo")
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

# -------------------------------------------------------------------
# VISTA PRINCIPAL
# -------------------------------------------------------------------
current_messages = st.session_state.chats[st.session_state.active_chat]

# Contenedor para el selector de modelo
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if len(current_messages) == 0:
        st.markdown('<h1 class="gemini-title">¿Por dónde empezamos?</h1>', unsafe_allow_html=True)
    
    modelo_seleccionado = st.selectbox(
        "Modalidad de Pancracio:",
        options=list(MODELOS_DISPONIBLES.keys()),
        index=0,
        label_visibility="collapsed" if len(current_messages) > 0 else "visible"
    )

# Mostrar mensajes anteriores si existen
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------------------------
# CAMPO DE ENTRADA (Siempre visible)
# -------------------------------------------------------------------
if prompt := st.chat_input("Preguntarle a Pancracio..."):
    
    full_prompt = prompt
    if file_text:
        full_prompt += f"\n\n[Contenido de {uploaded_file.name}]:\n{file_text}"

    user_msg = {"role": "user", "content": full_prompt}
    current_messages.append(user_msg)

    # Si es el primer mensaje, recargar pantalla para ocultar el título central
    if len(current_messages) == 1:
        st.rerun()

    with st.chat_message("user"):
        st.markdown(prompt)
        if file_text:
            st.info(f"📄 Documento adjunto: {uploaded_file.name}")

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        api_messages = [{"role": m["role"], "content": m["content"]} for m in current_messages]
        model_code = MODELOS_DISPONIBLES[modelo_seleccionado]
        
        try:
            response = client.chat.completions.create(
                model=model_code,
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
