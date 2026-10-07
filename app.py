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
# ESTILOS CSS PERSONALIZADOS
# -------------------------------------------------------------------
st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

<style>
    /* Fondo principal estilo Dark Neón */
    .stApp {
        background: radial-gradient(circle at 50% 45%, #180a0e 0%, #0d0a0f 60%, #050406 100%);
        color: #e2e8f0;
    }

    #MainMenu, header, footer {visibility: hidden;}

    /* Sidebar Ultra Estrecho */
    section[data-testid="stSidebar"] {
        width: 80px !important;
        background-color: #090a0d !important;
        border-right: 1px solid rgba(255, 42, 95, 0.2);
    }

    div[data-testid="stSidebarUserContent"] {
        padding: 1.2rem 0.2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Animación del Logo Estrella (Sparkle) */
    @keyframes pulseGlow {
        0% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 8px rgba(255, 42, 95, 0.7)); }
        50% { transform: scale(1.18) rotate(180deg); filter: drop-shadow(0 0 18px rgba(255, 82, 82, 1)); }
        100% { transform: scale(1) rotate(360deg); filter: drop-shadow(0 0 8px rgba(255, 42, 95, 0.7)); }
    }

    .sparkle-icon {
        font-size: 2.2rem;
        display: inline-block;
        margin-bottom: 1.2rem;
        animation: pulseGlow 5s infinite ease-in-out;
        background: linear-gradient(135deg, #ff2a5f 0%, #ff5252 50%, #d90429 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        cursor: pointer;
    }

    /* Estilo para los botones de íconos en la barra lateral */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 42, 95, 0.1) !important;
        color: #94a3b8 !important;
        font-size: 1.2rem !important;
        border-radius: 14px !important;
        width: 50px !important;
        height: 50px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto 0.8rem auto !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 42, 95, 0.2) !important;
        color: #ffffff !important;
        border-color: #ff2a5f !important;
        transform: translateY(-2px) scale(1.08);
        box-shadow: 0 0 16px rgba(255, 42, 95, 0.5) !important;
    }

    /* Título Gemini */
    .gemini-title {
        font-size: 2.8rem;
        font-weight: 600;
        color: #f1f5f9;
        text-align: center;
        margin-top: 6vh;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }

    /* Estilo de los chats */
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
# CLIENTE GROQ
# -------------------------------------------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró la variable GROQ_API_KEY en los Secrets de Streamlit.")
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

if "edu_mode" not in st.session_state:
    st.session_state.edu_mode = False

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if "show_file_upload" not in st.session_state:
    st.session_state.show_file_upload = False

if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

# -------------------------------------------------------------------
# BARRA LATERAL CON ÍCONOS ESTILIZADOS
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div style="text-align:center;"><span class="sparkle-icon">✦</span></div>', unsafe_allow_html=True)

    if st.button("✏️", help="Nuevo Chat"):
        num = len(st.session_state.chats) + 1
        name = f"Chat {num}"
        st.session_state.chats[name] = []
        st.session_state.active_chat = name
        st.session_state.show_history = False
        st.rerun()

    if st.button("🔍", help="Historial y Búsqueda"):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()

    edu_icon = "🎓" if not st.session_state.edu_mode else "💡"
    if st.button(edu_icon, help="Modo Tutor / Educación Paso a Paso"):
        st.session_state.edu_mode = not st.session_state.edu_mode
        status = "Activado" if st.session_state.edu_mode else "Desactivado"
        st.toast(f"Modo Tutor {status}")

    if st.button("📎", help="Adjuntar Documentos"):
        st.session_state.show_file_upload = not st.session_state.show_file_upload
        st.rerun()

    st.markdown("<div style='margin-top: 20vh;'></div>", unsafe_allow_html=True)

    if st.button("⚙️", help="Configuración del Modelo"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()

    st.markdown('<div style="text-align: center; font-size: 1.5rem; margin-top: 0.5rem;" title="Usuario Activo">🤖</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# PANELES DESPLEGABLES
# -------------------------------------------------------------------
if st.session_state.show_history:
    with st.expander("📚 **Historial de Conversaciones**", expanded=True):
        chat_list = list(st.session_state.chats.keys())
        selected = st.radio(
            "Selecciona un chat:",
            options=chat_list,
            index=chat_list.index(st.session_state.active_chat)
        )
        if selected != st.session_state.active_chat:
            st.session_state.active_chat = selected
            st.rerun()

file_content = ""
if st.session_state.show_file_upload:
    with st.expander("📁 **Cargar Archivo de Texto o Código**", expanded=True):
        uploaded_file = st.file_uploader("Sube un archivo (.txt, .py, .md):", type=["txt", "py", "md"])
        if uploaded_file:
            try:
                file_content = uploaded_file.getvalue().decode("utf-8")
                st.success(f"📄 Archivo '{uploaded_file.name}' listo para enviarse.")
            except Exception:
                st.error("Error al leer el archivo.")

if st.session_state.show_settings:
    with st.expander("⚙️ **Configuración Avanzada**", expanded=True):
        st.session_state.temperature = st.slider(
            "Creatividad del modelo (Temperature):",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1
        )

# -------------------------------------------------------------------
# ÁREA PRINCIPAL DE CHAT
# -------------------------------------------------------------------
current_messages = st.session_state.chats[st.session_state.active_chat]

if st.session_state.edu_mode:
    st.info("🎓 **Modo Tutor Activo:** Pancracio explicará con ejemplos detallados y didácticos.")

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if len(current_messages) == 0:
        st.markdown('<h1 class="gemini-title">¿Por dónde empezamos?</h1>', unsafe_allow_html=True)
    
    modelo_seleccionado = st.selectbox(
        "Modelo de IA:",
        options=list(MODELOS_DISPONIBLES.keys()),
        index=0,
        label_visibility="collapsed" if len(current_messages) > 0 else "visible"
    )

# Renderizar mensajes guardados previamente
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------------------------
# ENTRADA Y GENERACIÓN DE RESPUESTAS (CORREGIDO SIN RERUN)
# -------------------------------------------------------------------
if prompt := st.chat_input("Preguntarle a Pancracio..."):
    
    full_prompt = prompt
    if file_content:
        full_prompt += f"\n\n[Contenido adjunto]:\n{file_content}"

    # 1. Agregar mensaje del usuario a la sesión
    user_msg = {"role": "user", "content": full_prompt}
    current_messages.append(user_msg)

    # 2. Renderizar mensaje del usuario en pantalla inmediatamente
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Generar y transmitir la respuesta del asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        system_instruction = []
        if st.session_state.edu_mode:
            system_instruction.append({
                "role": "system", 
                "content": "Eres un tutor didáctico. Explica los conceptos paso a paso con ejemplos claros y estructurados."
            })
            
        api_messages = system_instruction + [{"role": m["role"], "content": m["content"]} for m in current_messages]
        model_code = MODELOS_DISPONIBLES[modelo_seleccionado]
        
        try:
            response = client.chat.completions.create(
                model=model_code,
                messages=api_messages,
                temperature=st.session_state.temperature,
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
            st.error(f"Error al conectar con la API: {e}")
