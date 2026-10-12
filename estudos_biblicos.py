"""
Luz & Palavra — Assistente de Estudos Bíblicos
Aplicação em Python + Streamlit + API Groq.

Instalação:
    pip install streamlit groq

Execução:
    streamlit run estudos_biblicos.py

Use sua chave de API Groq no campo da barra lateral.
Nunca publique sua chave de API no GitHub.
"""

import streamlit as st
from groq import Groq

# --------------------------- Configuração da página ---------------------------
st.set_page_config(
    page_title="Luz & Palavra | Estudos Bíblicos",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- Estilo visual ------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 90% 3%, rgba(203, 169, 106, 0.13), transparent 26%),
            linear-gradient(180deg, #fbfaf6 0%, #f4f1e8 100%);
        color: #26352d;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #173b31 0%, #102a23 100%);
    }
    [data-testid="stSidebar"] * { color: #f7f4eb !important; }
    [data-testid="stSidebar"] input {
        color: #20372e !important;
        background: #fffdf8 !important;
    }
    .hero {
        padding: 2.0rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(120deg, #173b31 0%, #285545 70%, #426a50 100%);
        color: #fffaf0;
        border: 1px solid rgba(255,255,255,.12);
        box-shadow: 0 14px 34px rgba(25, 55, 42, .14);
        margin-bottom: 1.3rem;
    }
    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif;
        color: #fffaf0;
        font-size: clamp(2rem, 4vw, 3.15rem);
        margin: 0 0 .4rem 0;
        line-height: 1.12;
    }
    .hero p { color: #e6eadf; font-size: 1.03rem; margin: 0; }
    .eyebrow {
        color: #e4c58b;
        text-transform: uppercase;
        letter-spacing: .16em;
        font-size: .72rem;
        font-weight: 700;
        margin-bottom: .7rem;
    }
    .section-card {
        background: rgba(255, 255, 255, .78);
        border: 1px solid #e7e0d2;
        padding: 1.1rem 1.25rem;
        border-radius: 18px;
        margin-bottom: .8rem;
    }
    .section-card h3 { color: #214637; margin-top: 0; }
    .small-muted { color: #68766d; font-size: .9rem; }
    /* Contraste geral: rótulos e textos dos controles sobre o fundo claro */
    .stApp, .stApp p, .stApp li, .stApp label,
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"] p {
        color: #26352d;
    }
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    .stApp label {
        color: #34473b !important;
        opacity: 1 !important;
    }
    /* Abas: cobre também os elementos internos que o Streamlit renderiza */
    div[data-testid="stTabs"] [role="tab"],
    div[data-testid="stTabs"] [role="tab"] *,
    div[data-testid="stTabs"] button,