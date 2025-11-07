import streamlit as st
import random
import pandas as pd

# ============================
# CONFIGURACIÓN DE PÁGINA
# ============================
st.set_page_config(
    page_title="Keyword Finder Pro+",
    page_icon="🚀",
    layout="centered"
)

# ============================
# ESTILOS
# ============================
st.markdown("""
    <style>
        body { background-color: #f8fafc; }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            max-width: 800px;
            margin: auto;
        }
        input, textarea, select {
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
        h1 { text-align: center; color: #1e3a8a; margin-bottom: 0.5rem; }
        h2 { text-align: center; color: #334155; margin-bottom: 1rem; }
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #6b7280;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================
# TÍTULOS
# ============================
st.markdown("<h1>🚀 Keyword Finder Pro+</h1>", unsafe_allow_html=True)
st.markdown("<h2>Generador avanzado de palabras clave para E-commerce</h2>", unsafe_allow_html=True)

# ============================
# ENTRADAS
# ============================
producto = st.text_input("🛒 Escribí una categoría o producto base:", placeholder="Ejemplo: zapatillas, auriculares, relojes...")

col1, col2 = st.columns(2)

with col1:
    idioma = st.selectbox("🌐 Idioma de las palabras clave", ["Español", "Inglés", "Portugués"])
    cantidad = st.slider("🔢 Cantidad de keywords", 5, 50, 20, step=5)

with col2:
    longitud = st.slider("🧩 Palabras por keyword", 1, 4, 2)
    complejidad = st.selectbox("⚙️ Nivel de complejidad", ["Básico", "Intermedio", "Avanzado"])

# ============================
# FUNCIONES
# ============================

def palabras_por_idioma(idioma):
    data = {
        "Español": {
            "tipos": ["barato", "oferta", "envío gratis", "nuevo", "tendencia", "moda", "2025", "lujo", "económico", "original"],
            "categorias": ["para mujer", "para hombre", "niños", "profesional", "deportiva", "inteligente"]
        },
        "Inglés": {
            "tipos": ["cheap", "sale", "new", "best", "premium", "trending", "original", "2025", "wireless", "smart"],
            "categorias": ["for men", "for women", "kids", "fashion", "luxury", "tech"]
        },
        "Portugués": {
            "tipos": ["barato", "oferta", "novo", "promoção", "moda", "luxo", "tendência", "inteligente"],
            "categorias": ["para homens", "para mulheres", "infantil", "esportivo", "tecnológico"]
        }
    }
    return data[idioma]


def generar_keywords(base, idioma, longitud, complejidad, cantidad):
    datos = palabras_por_idioma(idioma)
    tipos = datos["tipos"]
    categorias = datos["categorias"]

    # Complejidad = cuán elaborado suena
    extra = {
        "Básico": ["barato", "nuevo", "oferta"],
        "Intermedio": ["premium", "calidad", "original"],
        "Avanzado": ["exclusivo", "edición limitada", "alta gama", "colección especial"]
    }[complejidad]

    combinaciones = []
    for _ in range(cantidad * 2):  # generamos más y filtramos después
        partes = [base]
        while len(partes) < longitud:
            partes.append(random.choice(tipos + categorias + extra))
        combinaciones.append(" ".join(partes))

    # Filtramos duplicados
    combinaciones = list(set(combinaciones))
    random.shuffle(combinaciones)
    return combinaciones[:cantidad]

# ============================
# BOTÓN DE GENERACIÓN
# ============================
if st.button("✨ Generar keywords personalizadas"):
    if not producto.strip():
        st.error("⚠️ Escribí un producto o categoría primero.")
    else:
        st.success("✅ Palabras clave generadas con éxito:")
        keywords = generar_keywords(producto.lower(), idioma, longitud, complejidad, cantidad)

        # Mostrar en columnas
        for kw in keywords:
            st.markdown(f"• {kw}")

        # Descargar CSV
        df = pd.DataFrame(keywords, columns=["Keyword"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Descargar keywords en CSV",
            data=csv,
            file_name=f"keywords_{producto}.csv",
            mime="text/csv"
        )

# ============================
# FOOTER
# ============================
st.markdown("""
<div class='footer'>
Hecho con 💙 para profesionales del e-commerce — Keyword Finder Pro+
</div>
""", unsafe_allow_html=True)
