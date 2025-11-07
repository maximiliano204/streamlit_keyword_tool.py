import streamlit as st
import random
import pandas as pd

# ============================
# CONFIGURACIÓN
# ============================
st.set_page_config(page_title="Keyword Finder Pro+", page_icon="🚀", layout="centered")

# ============================
# ESTILOS
# ============================
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        max-width: 800px;
        margin: auto;
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
</style>
""", unsafe_allow_html=True)

# ============================
# TÍTULOS
# ============================
st.markdown("<h1>🚀 Keyword Finder Pro+</h1>", unsafe_allow_html=True)
st.markdown("<h2>Generador inteligente de palabras clave</h2>", unsafe_allow_html=True)

# ============================
# ENTRADAS
# ============================
producto = st.text_input("🛒 Producto o categoría base:", placeholder="Ejemplo: zapatillas, auriculares, relojes...")

col1, col2 = st.columns(2)
with col1:
    idioma = st.selectbox("🌐 Idioma", ["Español", "Inglés", "Portugués"])
    cantidad = st.slider("🔢 Cantidad de keywords", 5, 50, 20, step=5)
with col2:
    longitud = st.slider("🧩 Palabras por keyword", 1, 4, 2)
    complejidad = st.selectbox("⚙️ Nivel de complejidad", ["Básico", "Intermedio", "Avanzado"])

# ============================
# PATRONES POR IDIOMA
# ============================

def patrones_por_idioma(idioma):
    if idioma == "Español":
        return [
            "comprar {p}", "mejores {p}", "oferta de {p}", "{p} en línea",
            "{p} profesional", "precio de {p}", "{p} para mujer", "{p} para hombre",
            "nuevo {p}", "accesorios para {p}", "{p} baratos", "venta de {p}"
        ]
    elif idioma == "Inglés":
        return [
            "buy {p}", "best {p}", "{p} online", "{p} for men", "{p} for women",
            "cheap {p}", "new {p}", "original {p}", "premium {p}", "2025 {p}"
        ]
    elif idioma == "Portugués":
        return [
            "comprar {p}", "melhores {p}", "promoção de {p}", "{p} online",
            "{p} barato", "{p} novo", "oferta de {p}", "acessórios para {p}"
        ]

# ============================
# COMPLEJIDAD
# ============================
def agregar_complejidad(keyword, nivel):
    extras = {
        "Básico": [],
        "Intermedio": ["2025", "envío gratis", "original", "calidad"],
        "Avanzado": ["edición limitada", "alta gama", "colección especial", "exclusivo"]
    }[nivel]

    if extras and random.random() < 0.5:
        return f"{keyword} {random.choice(extras)}"
    return keyword

# ============================
# GENERADOR
# ============================
def generar_keywords(producto, idioma, longitud, complejidad, cantidad):
    producto = producto.strip().lower()
    patrones = patrones_por_idioma(idioma)
    combinaciones = []

    for _ in range(cantidad * 3):
        base = random.choice(patrones).replace("{p}", producto)
        kw = agregar_complejidad(base, complejidad)
        palabras = kw.split()
        if len(palabras) <= longitud:
            combinaciones.append(kw)

    combinaciones = list(set(combinaciones))
    random.shuffle(combinaciones)
    return combinaciones[:cantidad]

# ============================
# BOTÓN
# ============================
if st.button("✨ Generar keywords adaptadas"):
    if not producto.strip():
        st.error("⚠️ Escribí un producto o categoría primero.")
    else:
        st.success("✅ Palabras clave generadas:")
        keywords = generar_keywords(producto, idioma, longitud, complejidad, cantidad)
        for kw in keywords:
            st.markdown(f"• {kw}")

        df = pd.DataFrame(keywords, columns=["Keyword"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv,
            file_name=f"keywords_{producto}.csv",
            mime="text/csv"
        )

# ============================
# FOOTER
# ============================
st.markdown("<p style='text-align:center;color:#64748b;margin-top:1rem;'>Hecho con 💙 — Keyword Finder Pro+ v2</p>", unsafe_allow_html=True)
