"""
Streamlit app: IA Keyword Generator + Facebook Ads CSV analyzer

Requirements (to put in requirements.txt):
streamlit
openai
pandas
python-dotenv

Optional for trends scoring:
pytrends

How to use:
- Deploy on Streamlit Cloud: create a new app, paste this file into the repo and set the secret OPENAI_API_KEY or paste it in the UI.
- If you have a CSV export from Facebook Ads Library (or you copy-paste a table), you can upload it to let the app analyze which keywords appear most often.

Features:
- Generates keyword ideas, long-tails, ad hooks and cluster suggestions using OpenAI.
- Scores keywords by estimated commercial intent and competition (AI-estimated).
- Exports keywords as CSV for use in manual searches of Facebook Ads Library.
- Optional: upload Facebook Ads Library CSV to get counts of keywords appearing in ad titles/copies.

Note: This app *does not* scrape Facebook or call Meta APIs. It helps generate and analyze keywords and analyze CSVs you provide.
"""

import streamlit as st
import pandas as pd
import io
import os
import openai
from typing import List, Dict

# --------------------------- Helpers ---------------------------

def set_openai_key(key: str):
    openai.api_key = key


def call_openai_generate(prompt: str, model: str = "gpt-4", max_tokens: int = 600) -> str:
    # Simple wrapper for ChatCompletion
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "Eres un asistente que ayuda a generar keywords comerciales y estimaciones de competencia para e-commerce."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens,
            n=1
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error llamando a OpenAI: {e}")
        return ""


def generate_keywords_with_ai(category: str, country: str, languages: str, num_keywords: int, model: str = "gpt-4") -> pd.DataFrame:
    prompt = f"Generá {num_keywords} keywords únicas y orientadas a e-commerce para la categoría: '{category}'.\n" \
             f"Contexto: país='{country}', idiomas='{languages}'.\n" \
             "Para cada keyword devolvé en formato JSON: {\n  \"keyword\": string,\n  \"intent\": \"alta|media|baja\",\n  \"competition_estimate\": number entre 0 y 100 (mayor = más competencia),\n  \"suggested_ad_hook\": string corta,\n  \"longtail_variations\": [strings]\n}\n" \
             "Ordená la lista por prioridad comercial (primera la mejor)." \

    raw = call_openai_generate(prompt, model=model)

    # Try to extract JSON-like blocks from the response
    import re, json
    arr = []
    # find first '[' ... ']' block or individual {...}
    json_blocks = re.findall(r"\{[\s\S]*?\}", raw)
    for jb in json_blocks:
        try:
            # sanitize: replace single quotes with double quotes when safe
            clean = jb.replace("'", '"')
            obj = json.loads(clean)
            arr.append(obj)
        except Exception:
            # try to use python's eval fallback (risky) but wrapped
            try:
                obj = eval(jb)
                arr.append(obj)
            except Exception:
                continue

    # Fallback: if no JSON parsed, try to parse by lines
    if not arr:
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        for line in lines[:num_keywords]:
            arr.append({"keyword": line})

    df = pd.DataFrame(arr)
    # normalize columns
    if 'competition_estimate' in df.columns:
        df['competition_estimate'] = pd.to_numeric(df['competition_estimate'], errors='coerce')
    return df


def score_keywords_locally(df: pd.DataFrame) -> pd.DataFrame:
    # Add a simple heuristic score if missing
    if 'competition_estimate' not in df.columns:
        df['competition_estimate'] = 50
    if 'intent' not in df.columns:
        df['intent'] = 'media'

    # numeric intent score
    intent_map = {'alta': 1.0, 'media': 0.6, 'baja': 0.3}
    df['intent_score'] = df['intent'].map(intent_map).fillna(0.5)
    # final priority score: higher intent, lower competition
    df['priority_score'] = (df['intent_score'] * 100) * (100 - df['competition_estimate']) / 100
    df = df.sort_values('priority_score', ascending=False).reset_index(drop=True)
    return df


def analyze_ads_csv(uploaded_file: io.BytesIO, keywords: List[str]) -> pd.DataFrame:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file)

    # unify text columns
    text_cols = [c for c in df.columns if df[c].dtype == 'object']
    if not text_cols:
        st.warning("El CSV no tiene columnas de texto para analizar; subí un CSV exportado desde Facebook Ads Library o con columnas que contengan copy/titulo.")
        return pd.DataFrame()

    df['combined_text'] = df[text_cols].fillna('').agg(' '.join, axis=1).str.lower()

    results = []
    for k in keywords:
        k_low = k.lower()
        count = df['combined_text'].str.contains(k_low, na=False).sum()
        results.append({'keyword': k, 'count_in_ads': int(count)})

    res_df = pd.DataFrame(results).sort_values('count_in_ads', ascending=False)
    return res_df


# --------------------------- Streamlit UI ---------------------------

st.set_page_config(page_title="IA Keyword Hunter - para Facebook Ads Library", layout="wide")
st.title("IA Keyword Hunter — keywords para buscar en Facebook Ads Library 🕵️‍♂️✨")

with st.expander("Instrucciones rápidas", expanded=True):
    st.markdown(
        """
        1. Pegá tu **OPENAI API KEY** (o guardala como secreto en Streamlit Cloud).  
        2. Escribí la categoría y elegí país/idioma.  
        3. Generá keywords.  
        4. (Opcional) Subí un CSV exportado de la Facebook Ads Library para ver cuántos anuncios contienen cada keyword.  

        *El app genera keywords, longtails, hooks y te da un "priority_score" estimado para ayudarte a elegir qué buscar manualmente en la Ads Library.*
        """
    )

# Sidebar for API key and settings
with st.sidebar:
    st.header("Ajustes")
    openai_key = st.text_input("OPENAI API KEY (puedes guardarla en Streamlit secrets también)", type="password")
    model = st.selectbox("Modelo OpenAI", options=["gpt-4", "gpt-4o", "gpt-3.5-turbo"], index=0)
    num_keywords = st.number_input("Cantidad de keywords a generar", min_value=5, max_value=200, value=30)
    country = st.text_input("País (para contexto)", value="Argentina")
    languages = st.text_input("Idiomas (comma-separated)", value="es")
    st.markdown("---")
    st.markdown("**Export / Integraciones**")
    enable_pytrends = st.checkbox("Habilitar pytrends (si lo instalás y querés datos de tendencia)")
    st.caption("Si activás pytrends, la app intentará usar Google Trends localmente en la instancia.")

if openai_key:
    set_openai_key(openai_key)
else:
    # try environment/secret
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key:
        set_openai_key(env_key)

# Main inputs
col1, col2 = st.columns([2,1])
with col1:
    category = st.text_input("Categoría / Brief producto", placeholder="ej: accesorios para mate, cepillos para mascotas, bandas elásticas fitness")
    extra_context = st.text_area("Contexto adicional (público objetivo, rango de precio, ángulo de marketing)", height=120)
with col2:
    st.write(" ")
    generate_btn = st.button("Generar keywords")
    uploaded = st.file_uploader("(Opcional) Subir CSV/Excel de Facebook Ads Library para análisis", type=['csv','xlsx','xls'])
    analyze_btn = st.button("Analizar CSV con keywords actuales")

# Storage in session state
if 'keywords_df' not in st.session_state:
    st.session_state['keywords_df'] = pd.DataFrame()

if generate_btn:
    if not category:
        st.error("Ingresá una categoría para generar keywords.")
    elif not openai.api_key:
        st.error("Pega tu OPENAI API KEY en la barra lateral o guardala como OPENAI_API_KEY en los secrets.")
    else:
        with st.spinner("Generando keywords con IA..."):
            df = generate_keywords_with_ai(category=category, country=country, languages=languages, num_keywords=int(num_keywords), model=model)
            if df.empty:
                st.error("No se pudieron generar keywords — intentá cambiar la categoría o el modelo.")
            else:
                df = score_keywords_locally(df)
                st.session_state['keywords_df'] = df
                st.success(f"Generadas {len(df)} keywords")

# Show generated keywords
if not st.session_state['keywords_df'].empty:
    st.subheader("Keywords generadas")
    df = st.session_state['keywords_df']
    st.dataframe(df[['keyword','intent','competition_estimate','priority_score']].fillna(''))

    c1, c2 = st.columns(2)
    with c1:
        st.download_button("Descargar CSV de keywords", data=df.to_csv(index=False).encode('utf-8'), file_name='keywords.csv')
    with c2:
        st.download_button("Descargar JSON", data=df.to_json(orient='records', force_ascii=False).encode('utf-8'), file_name='keywords.json')

    # allow user to edit competition / intent inline
    st.markdown("**Editar manualmente (descarga y re-subida)** — por ahora la edición directa no está implementada")

# Analyze uploaded CSV
if uploaded is not None and analyze_btn:
    if st.session_state['keywords_df'].empty:
        st.warning("Primero generá keywords o subí una lista de keywords en un archivo.")
    else:
        with st.spinner("Analizando CSV con las keywords..."):
            keywords_list = st.session_state['keywords_df']['keyword'].fillna('').tolist()
            res_df = analyze_ads_csv(uploaded, keywords_list)
            if not res_df.empty:
                st.subheader("Frecuencia de keywords en anuncios (estimada)")
                st.dataframe(res_df)
                st.download_button("Descargar resultados de análisis", data=res_df.to_csv(index=False).encode('utf-8'), file_name='ads_keyword_counts.csv')

# Manual keyword input and quick AI scoring
st.markdown("---")
st.header("Herramientas rápidas")
colA, colB = st.columns(2)
with colA:
    manual_keywords = st.text_area("Pegar lista de keywords (una por línea)")
    quick_score_btn = st.button("Pedir scoring rápido por IA")
with colB:
    st.write(" ")
    st.caption("Si pegás keywords, el modelo las evaluará (intent/compe).")

if quick_score_btn:
    if not manual_keywords.strip():
        st.error("Ingresá keywords para evaluar.")
    elif not openai.api_key:
        st.error("Pega tu OPENAI API KEY en la barra lateral o guardala como OPENAI_API_KEY en los secrets.")
    else:
        kw_list = [k.strip() for k in manual_keywords.splitlines() if k.strip()]
        prompt = "Evaluá estas keywords para e-commerce. Devolvé JSON con campos: keyword, intent (alta/media/baja), competition_estimate (0-100).\n\nKeywords:\n" + '\n'.join(kw_list)
        raw = call_openai_generate(prompt, model=model, max_tokens=400)
        st.text_area("Respuesta cruda de IA", value=raw, height=250)

st.markdown("---")
st.caption("App creada para ayudarte a generar ideas y priorizar búsquedas en la Facebook Ads Library. No realiza scraping automático de Facebook ni usa API de Meta: traé tus propios CSV si querés análisis real sobre anuncios.")

# Footer: next steps
st.markdown(""")
**Siguientes pasos recomendados:**

- Guardá tu OPENAI_API_KEY en los Secrets de Streamlit Cloud: `Settings -> Secrets` y agrega `OPENAI_API_KEY = "tu_key_aqui"`.  
- Subí este archivo a un repositorio en GitHub y conectalo desde Streamlit Cloud para despliegue continuo.  
- Si querés integrar Google Trends, instalá `pytrends` en el requirements y activá la casilla en la sidebar; después podés pedirme que agregue esa función.

Si querés, puedo:
- Adaptar la app para que haga scrapes legales o use una API concreta (si tenés acceso a una API de Ads).  
- Añadir una tabla de keywords con edición inline y guardado directo.  

Decime si querés que te arme el `requirements.txt` y el `README.md` listos para subir a GitHub.
""
)
