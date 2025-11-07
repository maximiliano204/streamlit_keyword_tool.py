import streamlit as st
import random
import time
import csv

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Keyword Finder Pro+ v3",
    page_icon="🔍",
    layout="centered"
)

# -------------------- CSS PERSONALIZADO --------------------
st.markdown("""
    <style>
    body {
        background: #f9fafb;
        font-family: 'Inter', sans-serif;
    }
    .main {
        background: white;
        padding: 3rem;
        border-radius: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: 0.3s ease-in-out;
    }
    h1 {
        color: #1f2937;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    h3 {
        color: #374151;
        font-weight: 600;
    }
    .stButton > button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        transform: scale(1.02);
    }
    .keyword-card {
        background: #f1f5f9;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        transition: 0.3s;
    }
    .keyword-card:hover {
        background: #e2e8f0;
        transform: translateX(3px);
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -------------------- FUNCIONES --------------------
def generar_keywords(base, idioma, cantidad, palabras, nivel, tipo):
    modificadores = {
        "SEO": ["mejor", "barato", "profesional", "opiniones", "guía", "tutorial", "recomendado", "2025", "online"],
        "Ads": ["comprar", "oferta", "nuevo", "promoción", "precio", "envío", "descuento", "calidad"],
        "Informacional": ["qué es", "cómo usar", "tipos de", "ideas para", "ejemplos de", "beneficios de"]
    }

    # Ajustar según nivel
    if nivel == "Básico":
        random.shuffle(modificadores[tipo])
        modificadores[tipo] = modificadores[tipo][:4]
    elif nivel == "Intermedio":
        modificadores[tipo] = modificadores[tipo]
    elif nivel == "Avanzado":
        modificadores[tipo] += ["análisis", "comparativa", "reviews", "tendencias", "estrategias"]

    keywords = []
    for _ in range(cantidad):
        mod = random.choice(modificadores[tipo])
        estructura = random.choice([
            f"{base} {mod}",
            f"{mod} {base}",
            f"{base} {mod} {random.choice(['alta calidad', 'profesional', '2025'])}",
        ])
        palabra_final = " ".join(estructura.split()[:palabras])
        keywords.append(palabra_final.strip())

    # Remover duplicados
    return list(dict.fromkeys(keywords))

# -------------------- UI --------------------
st.title("🔍 Generador profesional de palabras clave")
st.markdown("### Personalizá tus keywords de forma precisa y profesional")

base = st.text_input("🛒 Producto o categoría base:", placeholder="Ejemplo: cortina mosquitero")

col1, col2 = st.columns(2)
with col1:
    idioma = st.selectbox("🌐 Idioma", ["Español", "Inglés", "Portugués"])
with col2:
    tipo = st.selectbox("🎯 Tipo de búsqueda", ["SEO", "Ads", "Informacional"])

col3, col4 = st.columns(2)
with col3:
    cantidad = st.slider("📊 Cantidad de keywords", 5, 50, 15)
with col4:
    palabras = st.slider("🔤 Palabras por keyword", 2, 6, 3)

nivel = st.selectbox("⚙️ Nivel de complejidad", ["Básico", "Intermedio", "Avanzado"])

st.markdown("---")

# -------------------- GENERACIÓN --------------------
if st.button("🚀 Generar keywords adaptadas"):
    if base.strip() == "":
        st.warning("Por favor, ingresá una palabra base.")
    else:
        with st.spinner("Generando combinaciones..."):
            for percent_complete in range(100):
                time.sleep(0.01)
                st.progress(percent_complete + 1)
        time.sleep(0.3)

        resultados = generar_keywords(base, idioma, cantidad, palabras, nivel, tipo)
        st.success("✅ Palabras clave generadas con éxito:")

        for kw in resultados:
            st.markdown(f"<div class='keyword-card'>• {kw}</div>", unsafe_allow_html=True)

        # Descargar CSV
        csv_data = "\n".join(resultados)
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv_data,
            file_name=f"keywords_{base}.csv",
            mime="text/csv"
        )

st.markdown("<br><center>💼 Hecho con ❤️ — Keyword Finder Pro+ v3</center>", unsafe_allow_html=True)
