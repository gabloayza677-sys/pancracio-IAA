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
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Barra con Animación Neón Rojo + Íconos)
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo principal oscuro */
    .stApp {
        background: radial-gradient(circle at 50% 45%, #180a0e 0%, #0d0a0f 60%, #050406 100%);
        color: #e2e8f0;
    }

    #MainMenu, header, footer {visibility: hidden;}

    /* Barra lateral ultra estrecha de íconos */
    section[data-testid="stSidebar"] {
        width: 75px !important;
        background-color: #0a0b0e !important;
        border-right: 1px solid rgba(255, 42, 95, 0.15);
    }

    div[data-testid="stSidebarUserContent"] {
        padding: 1.2rem 0.2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* ANIMACIÓN DEL LOGO DE ESTRELLA NEÓN ROJO */
    @keyframes pulseGlow {
        0% {
            transform: scale(1) rotate(0deg);
            filter: drop-shadow(0 0 6px rgba(255, 42, 95, 0.6));
        }
        50% {
            transform: scale(1.15) rotate(180deg);
            filter: drop-shadow(0 0 16px rgba(255, 82, 82, 0.9));
        }
        100% {
            transform: scale(1) rotate(360deg);
            filter: drop-shadow(0 0 6px rgba(255, 42, 95, 0.6));
        }
    }

    .sparkle-icon {
        font-size: 1.8rem;
        display: inline-block;
        margin-bottom: 1.5rem;
        animation: pulseGlow 6s infinite ease-in-out;
        background: linear-gradient(135deg, #ff2a5f 0%, #ff5252 50%, #d90429 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        cursor: pointer;
    }

    /* Estilos para los botones de íconos en la barra lateral */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        font-size: 1.35rem !important;
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto 0.7rem auto !important;
        box-shadow: none !important;
        transition: all 0.25s ease-in-out !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 42, 95, 0.15) !important;
        color: #ff5252 !important;
        transform: scale(1.12);
        box-shadow: 0 0 12px rgba(255, 42, 95, 0.3) !important;
    }

    /* Título principal estilo Gemini */
    .gemini-title {
        font-size: 2.8rem;
        font-weight: 600;
        color: #f1f5f9;
        text-align: center;
        margin-top: 8vh;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }

    /* Contenedores de chat */
    .stChatMessage {
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(255, 42, 95, 0.08);
        border: 1px solid rgba(255, 42, 95, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# CONEXIÓN GROQ
# -------------------------------------------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró la variable GROQ_API_KEY en los Secrets.")
    st.stop()

client = Groq(api_key=groq_api_key)

MODELOS_DISPONIBLES = {
    "⚡ Pancracio Flash": "openai/gpt-oss-20b",
    "🧠 Pancracio Pro": "openai/gpt-oss-20b",
    "🎨 Pancracio Creativo": "openai/gpt-oss-20b"
}

# -------------------------------------------------------------------
# ESTADO DE LA SESIÓN
# -------------------------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Nuevo Chat": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Nuevo Chat"

# -------------------------------------------------------------------
# BARRA LATERAL CON ÍCONOS Y ANIMACIÓN NEÓN ROJO
# -------------------------------------------------------------------
with st.sidebar:
    # Logo animado de estrella brillante en tonos rojos
    st.markdown('<div style="text-align:center;"><span class="sparkle-icon">✦</span></div>', unsafe_allow_html=True)
    
    # 1. Nuevo Chat
    if st.button("✏️", help="Nuevo Chat"):
        num = len(st.session_state.chats) + 1
        name = f"Chat {num}"
        st.session_state.chats[name] = []
        st.session_state.active_chat = name
        st.rerun()

    # 2. Explorar
    if st.button("🔍", help="Explorar Desafíos"):
        st.toast("Modo Explorar activado")

    # 3. Educación / Capacitación
    if st.button("🎓", help="Modo Educación"):
        st.toast("Modo Educación activado")

    # 4. Modos / Plantillas
    if st.button("🖼️", help="Módulos de Trabajo"):
        st.toast("Cargando módulos")

    # 5. Apps / Herramientas
    if st.button("🎛️", help="Herramientas"):
        st.toast("Herramientas avanzadas")

    # Espacio para empujar los íconos inferiores abajo
    st.markdown("<div style='margin-top: 18vh;'></div>", unsafe_allow_html=True)

    # 6. Configuración
    if st.button("⚙️", help="Ajustes"):
        st.toast("Panel de Configuración")

    # 7. Perfil / Usuario
    st.markdown('<div style="text-align: center; font-size: 1.4rem; cursor: pointer;" title="Perfil">🤖</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# ÁREA PRINCIPAL
# -------------------------------------------------------------------
current_messages = st.session_state.chats[st.session_state.active_chat]

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if len(current_messages) == 0:
        st.markdown('<h1 class="gemini-title">¿Por dónde empezamos?</h1>', unsafe_allow_html=True)
    
    modelo_seleccionado = st.selectbox(
        "Modelo:",
        options=list(MODELOS_DISPONIBLES.keys()),
        index=0,
        label_visibility="collapsed" if len(current_messages) > 0 else "visible"
    )

# Renderizado de mensajes
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("Preguntarle a Pancracio..."):
    
    user_msg = {"role": "user", "content": prompt}
    current_messages.append(user_msg)

    if len(current_messages) == 1:
        st.rerun()

    with st.chat_message("user"):
        st.markdown(prompt)

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
