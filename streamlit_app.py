import streamlit as st
from openai import OpenAI
import config
import pandas as pd
from nltk.corpus import stopwords
import nltk
from components.comparison import get_gpt_explanation
from utills.data_processing import calculate_similarity
from components.job_offers import display_job_offers
from components.candidates import display_candidates
from google_sheets import read_sheet
from utills.visualization import display_bar_chart
from streamlit_echarts import st_echarts

# Configuración de la página
st.set_page_config(page_title="NLPMatchJobs", layout="wide")

st.markdown("""
<style>
    .reportview-container {
        background: #556DAC
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: #556DAC;
    }
    h1, h2, h3 {
        color: #1E3A8A;
        text-align: center;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        display: block;
        margin: 0 auto;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    .centered {
        display: flex;
        justify-content: center;
    }
    .metrics-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }
    .metric-item {
        margin: 10px;
        text-align: center;
    }
    .section-divider {
        border-top: 2px solid #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    .stMetric {
        text-align: center;
    }
    .stats-table {
        margin: 0 auto;
        width: 50%;
    }
    .stats-table th, .stats-table td {
        text-align: center;
        padding: 10px;
        border: 1px solid #1E3A8A;
    }
    .stats-table th {
        background-color: #f79b77;
        color: white;
    }
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    .comparison-result {
        background-color: #f0f4f8;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .comparison-card {
        background-color: white;
        border: 2px solid #4a5568;
        border-radius: 8px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .offer-card, .candidate-card {
        border-color: #2b6cb0;
    }
    .similarity-score {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .section-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .menu-title {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .menu-options {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ... (rest of the imports and configurations remain the same)

def main():
    # ... (previous code remains the same)

    try:
        # Cargar datos de ofertas y candidatos
        worksheet_jobs = read_sheet(credentials= config.credentials,range_val='Hoja 1')
        job_offers_data = worksheet_jobs
        
        worksheet_candidates = read_sheet(credentials=config.credentials,range_val='Hoja 2')
        candidates_data = worksheet_candidates
        
        # Mostrar ofertas
        st.markdown('<h2 class="section-title">OFERTAS DE TRABAJO</h2>', unsafe_allow_html=True)
        display_job_offers(job_offers_data)
        
        # Agregar línea divisora y espacio
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Mostrar candidatos
        st.markdown('<h2 class="section-title">CANDIDATOS</h2>', unsafe_allow_html=True)
        display_candidates(candidates_data)
        
        st.markdown('<br><br>', unsafe_allow_html=True)

        # Mostrar menú desplegado centrado
        st.markdown('<h3 class="menu-title">Opciones de visualización</h3>', unsafe_allow_html=True)
        st.markdown('<div class="menu-options">', unsafe_allow_html=True)
        st.button('Ver formación')
        st.button('Ver conocimientos')
        st.button('Ver experiencia')
        st.button('Ver funciones')
        st.markdown('</div>', unsafe_allow_html=True)

        # ... (rest of the code remains the same)

    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

if __name__ == "__main__":
    main()
