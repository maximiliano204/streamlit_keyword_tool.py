import streamlit as st
import random

# ============================
# CONFIGURACIÓN DE LA PÁGINA
# ============================
st.set_page_config(
    page_title="Keyword Finder Pro",
    page_icon="🔍",
    layout="centered"
)

# ============================
# ESTILOS PERSONALIZADOS
# ============================
st.markdown("""
    <style>
        body { background-color: #f8fafc; }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            margin: auto;
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
        h1 { text-align: center; color: #1e3a8a; }
        h2 { text-align: center; color: #334155; }
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
st.markdown("<h1>🔍 Keyword Finder Pro</h1>", unsafe_allow_html=True)
st.markdown("<h2>Encuentra palabras clave útiles para tu e-commerce sin IA</h2>", unsafe_allow_html=True)
st.write("")

# ============================
# ENTRADA DE USUARIO
# ============================
producto = st.text_input("💬 Escribí una categoría o producto:", placeholder="Ejemplo: zapatillas, auriculares, relojes...")

# ============================
# GENERADOR DE PALABRAS CLAVE
# ============================
def generar_keywords(base):
    comunes = ["barato", "oferta", "tienda online", "dropshipping", "nuevo", "envío gratis", "tendencia", "moda", "original", "calidad premium"]
    tipos = ["gamer", "bluetooth", "inalámbrico", "recargable", "smart", "para mujer", "para hombre", "2025", "de lujo", "personalizado"]

    palabras_base = [base, f"{base}s", f"{base} {random.choice(tipos)}", f"{base} {random.choice(comunes)}"]

    combinaciones = [f"{base} {t}" for t in tipos] + [f"{base} {c}" for c in comunes]

    sugerencias = list(set(palabras_base + combinaciones))
    random.shuffle(sugerencias)
    return sugerencias[:20]

# ============================
# BOTÓN DE GENERACIÓN
# ============================
if st.button("✨ Generar palabras clave"):
    if not producto.strip():
        st.error("⚠️ Escribí un producto o categoría primero.")
    else:
        st.success("✅ Palabras clave sugeridas:")
        palabras = generar_keywords(producto.lower())
        for p in palabras:
            st.markdown(f"• {p}")

        st.info("💡 Consejo: copiá estas palabras y usalas directamente en la [Biblioteca de anuncios de Facebook](https://www.facebook.com/ads/library/) para descubrir productos en tendencia.")

# ============================
# FOOTER
# ============================
st.markdown("""
<div class='footer'>
Hecho con 💙 por un creador de e-commerce — versión sin IA
</div>
""", unsafe_allow_html=True)
