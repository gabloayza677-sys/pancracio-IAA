import base64
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

# Función para codificar imágenes a Base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

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
    st.subheader("📁 Subir Archivo / Imagen")
    uploaded_file = st.file_uploader(
        "Adjunta una imagen o documento",
        type=["png", "jpg", "jpeg", "txt"]
    )
    
    if uploaded_file:
        st.success(f"Archivo cargado: {uploaded_file.name}")

# -------------------------------------------------------------------
# ÁREA PRINCIPAL DEL CHAT
# -------------------------------------------------------------------
st.title(f"📌 {st.session_state.active_chat}")

current_messages = st.session_state.chats[st.session_state.active_chat]

# Mostrar historial de mensajes
for message in current_messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], str):
            st.markdown(message["content"])
        elif isinstance(message["content"], list):
            for item in message["content"]:
                if item.get("type") == "text":
                    st.markdown(item["text"])
                elif item.get("type") == "image_url":
                    st.image(item["image_url"]["url"], caption="Imagen analizada", width=300)

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje para Pancracio..."):
    
    # Preparar el contenido del mensaje
    user_content = []
    
    if uploaded_file and uploaded_file.type.startswith("image"):
        base64_image = encode_image(uploaded_file)
        mime_type = uploaded_file.type
        image_url = f"data:{mime_type};base64,{base64_image}"
        
        user_content.append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })
        # Seleccionar modelo con capacidad de visión
        model_to_use = "llama-3.2-11b-vision-preview"
    else:
        # Modelo estándar para texto puro
        model_to_use = "llama-3.1-8b-instant"

    user_content.append({"type": "text", "text": prompt})

    user_msg = {"role": "user", "content": user_content}
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        if uploaded_file and uploaded_file.type.startswith("image"):
            st.image(uploaded_file, width=300)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Preparar historial limpio para la API
        api_messages = []
        for m in current_messages:
            api_messages.append({"role": m["role"], "content": m["content"]})
        
        try:
            response = client.chat.completions.create(
                model=model_to_use,
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
