# streamlit_keyword_tool.py
import streamlit as st
import google.generativeai as genai

# ===============================
# ⚙️ CONFIGURACIÓN DE LA APP
# ===============================
st.set_page_config(
    page_title="Keyword Finder AI",
    page_icon="🔍",
    layout="centered"
)

# ===============================
# 🎨 ESTILOS PERSONALIZADOS
# ===============================
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
    font-family: "Inter", sans-serif;
    color: #222;
}
h1 {
    color: #1a73e8;
    text-align: center;
    font-weight: 700;
}
h3 {
    color: #555;
    text-align: center;
    font-weight: 400;
    margin-bottom: 2rem;
}
.stTextInput>div>div>input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
}
.stButton>button {
    background: linear-gradient(90deg, #1a73e8, #4dabf7);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    padding: 0.6rem 1.2rem;
}
.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #1669c1, #3d91e0);
}
.result-box {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    color: #333;
    white-space: pre-wrap;
    font-size: 0.95rem;
    animation: fadeIn 0.8s ease;
}
.copy-btn {
    display: flex;
    justify-content: right;
    margin-top: 0.5rem;
}
.copy-btn button {
    background-color: #e9ecef;
    color: #1a73e8;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.3s;
}
.copy-btn button:hover {
    background-color: #1a73e8;
    color: white;
}
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #888;
    margin-top: 2rem;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 FUNCIÓN PARA GENERAR KEYWORDS
# ===============================
# --- Generador de Keywords con Gemini ---
import google.generativeai as genai

# Botón para generar
if st.button("✨ Generar keywords"):
    if not api_key or not categoria:
        st.warning("⚠️ Por favor, ingresá tu API Key y escribí una categoría antes de continuar.")
    else:
        with st.spinner("Generando palabras clave rentables... 🔍"):
            try:
                # Configurar la API
                genai.configure(api_key=api_key)

                # Crear el prompt
                prompt = f"""
                Sos un experto en marketing y e-commerce.
                Generá una lista de al menos 20 palabras clave muy rentables, relevantes y variadas
                para buscar productos exitosos en la biblioteca de anuncios de Facebook,
                basadas en la categoría o nicho: "{categoria}".

                Formato de salida:
                - Lista en viñetas o columnas
                - Sin texto adicional
                """

                # Generar texto con el modelo
                response = genai.generate_text(
                    model="models/gemini-1.5-flash",  # modelo actual y soportado
                    prompt=prompt
                )

                # Extraer resultado
                if hasattr(response, "result"):
                    output = response.result
                else:
                    output = response.candidates[0].output_text

                # Mostrar resultado
                st.success("✅ Palabras clave generadas con éxito:")
                st.markdown(f"### 📋 Resultados para **{categoria}**")
                st.markdown(output)

                # Opción para copiar fácilmente
                st.code(output, language="markdown")
                st.caption("💡 Copiá estas palabras y usalas directamente en la biblioteca de anuncios de Facebook.")

            except Exception as e:
                st.error(f"❌ Error al conectar con Gemini: {e}")


# ===============================
# 🧩 INTERFAZ DE USUARIO
# ===============================
st.title("🔍 Keyword Finder AI (Gemini Edition)")
st.markdown("<h3>Encuentra palabras clave rentables para tus búsquedas en la biblioteca de anuncios</h3>", unsafe_allow_html=True)
st.divider()

# Campo para API Key
api_key = st.text_input("🔑 Tu API Key de Google Gemini:", type="password", placeholder="Ej: AIzaSy...")

# Campo para categoría
category = st.text_input("🧠 Escribí una categoría o nicho:", placeholder="Ej: fitness, hogar, mascotas...")

# Botón principal
generate = st.button("✨ Generar keywords")

# Resultado
if generate:
    if not category.strip():
        st.warning("Por favor, escribí una categoría antes de generar.")
    else:
        keywords = generate_keywords(category, api_key)
        if keywords:
            st.markdown(f"<div class='result-box' id='result-box'>{keywords}</div>", unsafe_allow_html=True)
            st.markdown("""
                <div class='copy-btn'>
                    <button onclick="navigator.clipboard.writeText(document.getElementById('result-box').innerText)">
                        📋 Copiar al portapapeles
                    </button>
                </div>
            """, unsafe_allow_html=True)

# ===============================
# 📎 FOOTER
# ===============================
st.markdown("<div class='footer'>Hecho con 💙 por un creador para creadores de e-commerce — Potenciado por Gemini AI</div>", unsafe_allow_html=True)
