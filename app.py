import os
import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(
    page_title="Pancracio IA",
    page_icon="🤖",
    layout="wide"
)

# Obtener la API key de Groq
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ No se encontró la variable GROQ_API_KEY. Configúrala en los Secrets de Streamlit Cloud.")
    st.stop()

# Inicializar cliente de Groq
client = Groq(api_key=groq_api_key)

# -------------------------------------------------------------------
# GESTIÓN DE ESTADO (Múltiples chats)
# -------------------------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Chat 1"

# -------------------------------------------------------------------
# BARRA LATERAL (Menú de chats y subida de archivos)
# -------------------------------------------------------------------
with st.sidebar:
    st.title("🤖 Pancracio IA")
    
    if st.button("➕ Nuevo Chat", use_container_width=True):
        new_chat_num = len(st.session_state.chats) + 1
        new_chat_name = f"Chat {new_chat_num}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.active_chat = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Mis Conversaciones")
    
    chat_list = list(st.session_state.chats.keys())
    selected_chat = st.radio(
        "Selecciona un chat:",
        options=chat_list,
        index=chat_list.index(st.session_state.active_chat)
    )
    st.session_state.active_chat = selected_chat

    st.markdown("---")
    st.subheader("📁 Subir Archivo Texto / Código")
    uploaded_file = st.file_uploader(
        "Adjunta un archivo de texto o código (ej: .txt, .py)",
        type=["txt", "py", "md"]
    )
    
    file_text_content = ""
    if uploaded_file:
        try:
            file_text_content = uploaded_file.getvalue().decode("utf-8")
            st.success(f"Archivo cargado: {uploaded_file.name}")
        except Exception as e:
            st.error("Error al leer el archivo de texto.")

# -------------------------------------------------------------------
# ÁREA PRINCIPAL DEL CHAT
# -------------------------------------------------------------------
st.title(f"📌 {st.session_state.active_chat}")

current_messages = st.session_state.chats[st.session_state.active_chat]

# Mostrar historial de mensajes
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje para Pancracio..."):
    
    # Si hay contenido de un archivo de texto, lo adjuntamos al mensaje
    full_prompt = prompt
    if file_text_content:
        full_prompt += f"\n\n[Contenido del archivo adjunto ({uploaded_file.name})]:\n{file_text_content}"

    user_msg = {"role": "user", "content": full_prompt}
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if file_text_content:
            st.info(f"📄 Archivo adjunto incluido: {uploaded_file.name}")

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Preparar historial simple para openai/gpt-oss-20b
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
