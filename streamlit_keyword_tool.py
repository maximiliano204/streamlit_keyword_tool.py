# streamlit_keyword_tool.py
import streamlit as st
from openai import OpenAI
import pyperclip

# ===============================
# ⚙️ CONFIGURACIÓN
# ===============================
st.set_page_config(
    page_title="Keyword Finder AI",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# 🎨 ESTILO CUSTOM
# ===============================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #ffffff;
    font-family: "Inter", sans-serif;
}
h1 {
    color: #36cfc9;
    text-align: center;
}
h3 {
    color: #a5a5a5;
    text-align: center;
    font-weight: 400;
    margin-bottom: 2rem;
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
    white-space: pre-wrap;
    color: #f0f0f0;
    font-size: 0.95rem;
}
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #888;
    margin-top: 2rem;
}
.copy-btn {
    display: flex;
    justify-content: right;
    margin-top: -0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 FUNCIÓN PARA OBTENER KEYWORDS
# ===============================
def generate_keywords(category: str, api_key: str) -> str:
    """Genera keywords con OpenAI"""
    if not api_key:
        st.error("⚠️ Debes ingresar tu API Key para continuar.")
        return ""

    try:
        client = OpenAI(api_key=api_key)
        with st.spinner("Generando ideas..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un experto en marketing digital y análisis de e-commerce. "
                            "Tu tarea es generar keywords específicas, rentables y actuales "
                            "para buscar productos en la Biblioteca de Anuncios de Facebook."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Genera una lista de 25 palabras clave relacionadas con el nicho '{category}'. "
                            "Incluye combinaciones amplias y long-tail, separadas por saltos de línea. "
                            "Evita oraciones completas, solo términos o frases cortas."
                        ),
                    },
                ],
                temperature=0.8,
                max_tokens=400,
            )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ Error al conectar con OpenAI: {e}")
        return ""

# ===============================
# 🧩 INTERFAZ PRINCIPAL
# ===============================
st.title("🔍 Keyword Finder AI")
st.markdown("<h3>Encuentra ideas rentables para tus búsquedas en la biblioteca de anuncios</h3>", unsafe_allow_html=True)

st.divider()

# Campo para API Key
api_key = st.text_input("🔑 Tu API Key de OpenAI:", type="password", placeholder="sk-...")

# Campo de categoría
category = st.text_input("🧠 Escribí una categoría o nicho:", placeholder="Ej: fitness, hogar, mascotas...")

# Botón principal
generate = st.button("✨ Generar keywords")

if generate:
    if not category.strip():
        st.warning("Por favor, escribí una categoría antes de generar.")
    else:
        keywords = generate_keywords(category, api_key)
        if keywords:
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(keywords)
            st.markdown("</div>", unsafe_allow_html=True)

            # Botón de copiar
            st.markdown("<div class='copy-btn'>", unsafe_allow_html=True)
            if st.button("📋 Copiar al portapapeles"):
                pyperclip.copy(keywords)
                st.success("✅ Keywords copiadas al portapapeles.")
            st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# 📎 FOOTER
# ===============================
st.markdown("<div class='footer'>Hecho con ❤️ para creadores de e-commerce — powered by GPT-4o-mini</div>", unsafe_allow_html=True)
