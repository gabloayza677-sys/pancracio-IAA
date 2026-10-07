import os
import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(
    page_title="Pancracio IA",
    page_icon="🤖",
    layout="wide"
)

# Obtener la API key de Groq desde los Secrets
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
    
    # Botón para crear un nuevo chat
    if st.button("➕ Nuevo Chat", use_container_width=True):
        new_chat_num = len(st.session_state.chats) + 1
        new_chat_name = f"Chat {new_chat_num}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.active_chat = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Mis Conversaciones")
    
    # Selector de chat activo
    chat_list = list(st.session_state.chats.keys())
    selected_chat = st.radio(
        "Selecciona un chat:",
        options=chat_list,
        index=chat_list.index(st.session_state.active_chat)
    )
    st.session_state.active_chat = selected_chat

    st.markdown("---")
    st.subheader("📁 Subir Archivo / Imagen")
    uploaded_file = st.file_uploader(
        "Adjunta una imagen o documento",
        type=["png", "jpg", "jpeg", "txt", "pdf"]
    )
    
    if uploaded_file:
        st.success(f"Archivo cargado: {uploaded_file.name}")

# -------------------------------------------------------------------
# ÁREA PRINCIPAL DEL CHAT
# -------------------------------------------------------------------
st.title(f"📌 {st.session_state.active_chat}")

# Obtener historial del chat activo
current_messages = st.session_state.chats[st.session_state.active_chat]

# Mostrar historial de mensajes
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], caption="Imagen adjunta", width=300)

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje para Pancracio..."):
    
    image_to_save = None
    if uploaded_file and uploaded_file.type.startswith("image"):
        image_to_save = uploaded_file

    user_msg = {"role": "user", "content": prompt}
    if image_to_save:
        user_msg["image"] = image_to_save

    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_to_save:
            st.image(image_to_save, caption="Imagen adjunta", width=300)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        api_messages = [{"role": m["role"], "content": m["content"]} for m in current_messages]
        
        try:
            # Modelo de producción activamente soportado en Groq
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
