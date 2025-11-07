# streamlit_keyword_tool.py
import streamlit as st
from openai import OpenAI
import time

# ===============================
# 🔑 Configuración de la app
# ===============================
st.set_page_config(
    page_title="Keyword Finder AI",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# 🎨 Estilo minimalista
# ===============================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #ffffff;
    font-family: "Inter", sans-serif;
}
h1, h2, h3 {
    color: #36cfc9;
}
.stTextInput>div>div>input {
    background-color: #1b1f24;
    color: #e6e6e6;
    border-radius: 10px;
}
.stButton>button {
    background-color: #36cfc9;
    color: #0e1117;
    border-radius: 8px;
    font-weight: 600;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #13a89e;
    color: white;
}
.result-box {
    background-color: #1b1f24;
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1rem;
}
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #888;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 Cliente de OpenAI
# ===============================
client = None

def set_openai_key(key: str):
    """Inicializa el cliente OpenAI"""
    global client
    if not key:
        client = None
        return
    client = OpenAI(api_key=key)

# ===============================
# ⚙️ Llamada a la IA
# ===============================
def generate_keywords(category: str) -> str:
    """Genera keywords a partir de una categoría de producto"""
    global client
    if client is None:
        st.error("⚠️ No se detectó tu API Key. Agrégala en los secrets de Streamlit.")
        return ""
    
    try:
        with st.spinner("Generando ideas..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing digital y análisis de anuncios. Generas keywords específicas, rentables y actuales para buscar productos en la Biblioteca de Anuncios de Facebook."},
                    {"role": "user", "content": f"Genera una lista de 20 palabras clave relevantes para el nicho '{category}'. Combina términos amplios, long-tails y relacionados a productos físicos que se vendan bien."}
                ],
                temperature=0.8,
                max_tokens=400
            )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error llamando a OpenAI: {e}")
        return ""

# ===============================
# 🧩 Interfaz principal
# ===============================
st.title("🔍 Keyword Finder AI")
st.subheader("Encuentra palabras clave ganadoras para e-commerce")

st.markdown("Escribí una **categoría o nicho** (por ejemplo: *fitness*, *mascotas*, *hogar*, *mate*, etc.) y la IA te dará ideas de keywords para buscar en la Biblioteca de Anuncios de Facebook.")

# API Key (desde los secrets o manual)
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    st.warning("No hay API Key configurada. Agregala en Settings → Secrets como `OPENAI_API_KEY`.")
else:
    set_openai_key(api_key)

# Campo de entrada
category = st.text_input("🧠 Escribí una categoría o nicho:", placeholder="Ej: accesorios para mate")

# Botón de acción
if st.button("✨ Generar keywords"):
    if category.strip():
        keywords = generate_keywords(category)
        if keywords:
            st.markdown(f"<div class='result-box'><pre>{keywords}</pre></div>", unsafe_allow_html=True)
    else:
        st.warning("Por favor, escribí una categoría antes de generar.")

# ===============================
# 📎 Footer
# ===============================
st.markdown("<div class='footer'>Hecho con ❤️ para creadores de e-commerce</div>", unsafe_allow_html=True)
