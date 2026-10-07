import os
import streamlit as st
from groq import Groq

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Pancracio IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Pancracio IA")
st.write("¡Hola! Soy Pancracio, tu asistente de Inteligencia Artificial.")

# Obtener la API key de Groq desde las variables de entorno / Secrets
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró la variable GROQ_API_KEY. Configúrala en los Secrets de Streamlit Cloud.")
    st.stop()

# Inicializar cliente de Groq
client = Groq(api_key=groq_api_key)

# Inicializar el historial de chat en la sesión si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Eres Pancracio, un asistente de IA muy amable, atento, servicial y divertido."
        }
    ]

# Mostrar los mensajes del historial (omitiendo el prompt de sistema)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Capturar la entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje para Pancracio..."):
    # Agregar mensaje del usuario al historial y mostrarlo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta del asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Consulta a la API de Groq con el modelo oficial Llama 3.3
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )

            # Transmitir (stream) la respuesta palabra por palabra
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            # Guardar la respuesta de Pancracio en el historial
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Ocurrió un error al procesar tu solicitud: {e}")
