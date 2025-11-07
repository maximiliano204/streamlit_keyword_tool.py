import streamlit as st
import google.generativeai as genai

# ============================
# CONFIGURACIÓN DE LA PÁGINA
# ============================
st.set_page_config(
    page_title="Keyword Finder AI (Gemini Edition)",
    page_icon="🔍",
    layout="centered"
)

# ============================
# ESTILOS PERSONALIZADOS
# ============================
st.markdown("""
    <style>
        body {
            background-color: #f8fafc;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            margin: auto;
            transition: all 0.3s ease-in-out;
        }
        input, textarea {
            border-radius: 12px !important;
            border: 1px solid #ddd !important;
            background-color: #fff !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, #2563eb, #1e40af);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #1d4ed8, #1e3a8a);
        }
        h1 {
            text-align: center;
            color: #1e3a8a;
        }
        h2 {
            text-align: center;
            color: #334155;
        }
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #6b7280;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================
# TÍTULO
# ============================
st.markdown("<h1>🔍 Keyword Finder AI (Gemini Edition)</h1>", unsafe_allow_html=True)
st.markdown("<h2>Encuentra palabras clave rentables para tus búsquedas en la biblioteca de anuncios</h2>", unsafe_allow_html=True)

# ============================
# CAMPOS DE ENTRADA
# ============================
st.write("")
api_key = st.text_input("🔑 Tu API Key de Google Gemini:", type="password", placeholder="Pega tu API Key aquí...")
user_input = st.text_input("💬 Escribí una categoría o nicho:", placeholder="Ejemplo: lámparas, relojes inteligentes, suplementos...")

# ============================
# FUNCIÓN PRINCIPAL
# ============================
def generate_keywords(api_key, prompt):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # ✅ Modelo correcto para la versión moderna del SDK
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"Genera 20 palabras clave útiles para buscar productos de e-commerce en la biblioteca de anuncios de Facebook sobre: {prompt}. "
            f"Devuélvelas separadas por comas, sin numeración ni texto adicional."
        )

        # Extraer el texto generado
        return response.text.strip()

    except Exception as e:
        return f"❌ Error al conectar con Gemini: {e}"

# ============================
# BOTÓN DE GENERACIÓN
# ============================
generate = st.button("✨ Generar keywords", key="generate_keywords_btn")

if generate:
    if not api_key.strip():
        st.error("⚠️ Por favor, ingresa tu API Key de Gemini antes de continuar.")
    elif not user_input.strip():
        st.error("⚠️ Escribí una categoría o nicho antes de generar las keywords.")
    else:
        with st.spinner("🧠 Generando palabras clave con IA..."):
            keywords = generate_keywords(api_key, user_input)

        if keywords.startswith("❌ Error"):
            st.error(keywords)
        else:
            st.success("✅ Palabras clave generadas con éxito:")
            st.markdown(f"<div class='main'>{keywords}</div>", unsafe_allow_html=True)

# ============================
# FOOTER
# ============================
st.markdown("""
<div class='footer'>
Hecho con 💙 para creadores de e-commerce — Potenciado por Gemini AI
</div>
""", unsafe_allow_html=True)
