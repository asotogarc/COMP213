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
        background-color: #f0f4f8;  /* Light blue-gray background */
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .comparison-card {
        background-color: white;
        border: 2px solid #4a5568;  /* Dark blue-gray border */
        border-radius: 8px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .offer-card, .candidate-card {
        border-color: #2b6cb0;  /* Darker blue border for offer and candidate cards */
    }
    .similarity-score {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
</style>
""", unsafe_allow_html=True)

# Apply custom theme



# Descargar stopwords en español
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# Definimos nuestra API Key de chat GPT
client = OpenAI(api_key=config.API_KEY)

def main():

    # Inicializar variables de sesión
    if 'selected_offer' not in st.session_state:
        st.session_state.selected_offer = None
    if 'selected_candidate' not in st.session_state:
        st.session_state.selected_candidate = None

    sheet_title = "MyNewSheets"

    try:
        # Cargar datos de ofertas y candidatos
        worksheet_jobs = read_sheet(credentials= config.credentials,range_val='Hoja 1')
        job_offers_data = worksheet_jobs
        
        worksheet_candidates = read_sheet(credentials=config.credentials,range_val='Hoja 2')
        candidates_data = worksheet_candidates
        
        # Mostrar ofertas y candidatos
        display_job_offers(job_offers_data)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)


        
        display_candidates(candidates_data)
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Ejecutar comparación automáticamente al seleccionar oferta y candidatura
        if st.session_state.selected_offer and st.session_state.selected_candidate:
            similarity, top_terms = calculate_similarity(st.session_state.selected_offer, st.session_state.selected_candidate)

            # Opinión personalizada del GPT
            gpt_opinion_prompt = f"""
            Analiza el texto de la oferta:
            {st.session_state.selected_offer}
            
            Y el texto de la candidatura:
            {st.session_state.selected_candidate}
            
            Basándonos en la información de la oferta {st.session_state.selected_offer} y en el de la candidatura {st.session_state.selected_candidate}, opinamos si la oferta se ajusta al perfil del candidato.
            Si la la oferta  se ajusta al perfil de la candidatura enseña un numero y un correo para poder ponerse en contacto con el candidato, no con la empresa que oferta el trabajo.
            No me tienes que dar un resumen del contenido de la oferta y la cnadidatura si no una conclusion desarrollado argumentando muy bien si la candidatura se ajusta bien a la oferta
            Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion = get_gpt_explanation(gpt_opinion_prompt)
            st.markdown('<h2 class="section-title">¿ENCAJA EL CANDIDATO CON LA OFERTA?</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="gpt-output">{gpt_opinion}</div>', unsafe_allow_html=True)
            
            
            # Mostrar resultados en tarjetas centradas
            st.markdown(f"""
            <div class="comparison-result" style="display: flex; justify-content: center;">
                <div class="comparison-card offer-card" style="margin: 0 10px;">
                    <h3>SIMIKITUD DE AMBOS TEXTOS</h3>
                    <h4>{st.session_state.selected_offer['Nombre']}</h4>
                    <p class="info-trigger">Ver información completa</p>
                        {similarity:.2f}%
                </div>

                </div>
              
            </div>
            """, unsafe_allow_html=True)


    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

if __name__ == "__main__":
    main()
