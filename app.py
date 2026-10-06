import streamlit as st
from groq import Groq

# 1. Configuración de la página web
st.set_page_config(
    page_title="EduAI | Tutor de Historia y Química",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS Personalizados para diseño moderno
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #68d391 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .feature-card {
        background-color: #1A1D24;
        border: 1px solid #2D3748;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    .feature-card h4 {
        color: #4FD1C5;
        margin-bottom: 5px;
    }
    [data-testid="stSidebar"] {
        background-color: #161922;
        border-right: 1px solid #2D3748;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Conexión con la API de Groq
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 4. Barra Lateral (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429149.png", width=70)
    st.title(" Panel del Tutor")
    st.markdown("---")
    
    @st.cache_data(ttl=600)
    def obtener_modelos_activos():
        try:
            models_data = client.models.list()
            # Excluimos modelos de audio, guard e identificamos los recomendados
            modelos = [m.id for m in models_data.data if "whisper" not in m.id and "guard" not in m.id]
            # Priorizar modelos LLaMA estables si existen en la lista
            modelos_ordenados = sorted(modelos, key=lambda x: ("llama" not in x.lower(), x))
            return modelos_ordenados
        except Exception:
            return ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"]

    modelos_disponibles = obtener_modelos_activos()
    modelo_seleccionado = st.selectbox("🧠 Modelo de IA:", modelos_disponibles)
    
    temperatura = st.slider("🔥 Creatividad (Temperatura):", 0.0, 1.0, 0.5, 0.1)
    
    st.markdown("---")
    st.markdown("### 💡 Ejemplos de uso")
    st.caption("• *¿Cuál fue la causa principal de la Primera Guerra Mundial?*")
    st.caption("• *Explícame el enlace covalente con un ejemplo sencillo.*")
    st.caption("• *Hazme un resumen en 3 puntos.*")
    
    if st.button("🗑️ Limpiar Conversación", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# 5. Banner Principal
st.markdown("""
    <div class="main-header">
        <h1>🎓 EduAI: Historia & Química</h1>
        <p>Tu asistente especializado con Inteligencia Artificial</p>
    </div>
""", unsafe_allow_html=True)

# 6. Tarjetas informativas superiores
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h4>📜 Módulo de Historia</h4>
            <p style="color: #A0AEC0; font-size: 0.9rem;">Líneas de tiempo, batallas, biografías y revoluciones.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h4>🧪 Módulo de Química</h4>
            <p style="color: #A0AEC0; font-size: 0.9rem;">Tabla periódica, estequiometría, enlaces y reacciones.</p>
        </div>
    """, unsafe_allow_html=True)

# 7. Prompt de Sistema
PROMPT_ESPECIALIZADO = """
Eres un tutor experto en Historia Universal y Química General.
Tus funciones principales son:
1. Responder dudas sobre procesos químicos, reacciones, tabla periódica y fórmulas.
2. Explicar eventos históricos, causas, consecuencias y fechas de manera cronológica.
3. Resolver problemas o hacer resúmenes desglosando paso a paso.
4. Si el usuario te pide resumir, responde de forma concisa utilizando puntos o viñetas directas.
5. Si te preguntan algo ajeno a historia o química, recuerda amablemente tu especialidad.
"""

# 8. Historial de chat
if "messages" not in st.session_state or len(st.session_state["messages"]) == 0:
    st.session_state["messages"] = [
        {"role": "system", "content": PROMPT_ESPECIALIZADO},
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu tutor personalizado. ¿Sobre qué tema de **Historia** o **Química** deseas aprender hoy?"}
    ]

# 9. Mostrar el Chat en pantalla
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# 10. Entrada del usuario y generación de respuestas
user_input = st.chat_input("Escribe tu pregunta de Historia o Química...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""

        # Gestión eficiente de tokens de entrada (System Prompt + últimos 4 mensajes)
        system_msg = [st.session_state.messages[0]]
        recent_msgs = [m for m in st.session_state.messages[1:] if m["role"] != "system"][-4:]
        mensajes_para_enviar = system_msg + recent_msgs

        try:
            stream = client.chat.completions.create(
                messages=mensajes_para_enviar,
                model=modelo_seleccionado,
                temperature=temperatura,
                max_tokens=500,  # Previene errores de cuota OTPM (Rate Limit Exceeded)
                stream=True
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error("⚠️ Ocurrió un inconveniente con el modelo seleccionado:")
            st.code(str(e))
            st.info("Sugerencia: Selecciona 'llama-3.1-8b-instant' o 'llama-3.3-70b-versatile' en la barra lateral.")