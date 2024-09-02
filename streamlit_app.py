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
# Apply custom theme
st.markdown("""
    <style>
    :root {
        --primary-color: #4CAF50;
        --background-color: #f0f2f6;
        --secondary-background-color: #e0e0e0;
        --text-color: #262730;
        --font: sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
# Enlazamos el archivo custom.css
with open("styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Descargar stopwords en español
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# Definimos nuestra API Key de chat GPT
client = OpenAI(api_key=config.API_KEY)

def main():
    st.title("EINNOVA 💼 | COMPARADOR DE CANDIDATURAS Y OFERTAS DE TRABAJO")

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
            Después de nuestra opinión, mencionamos que mostraremos los resultados del análisis del procesamiento del lenguaje natural de ambos textos. En el caso de que el candidato no encaje con la oferta describirle en que areas puede mejorar y recomendarle libros, cursos, vídeos, etcétera.
            Debes explicar sencillamente y brevemente que puede haber candidatos que se ajustan bien a un perfil pero que la comparación del texto de su candidatura con el de la oferta puede presentar un  bajo porcentaje de similitud
            Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion = get_gpt_explanation(gpt_opinion_prompt)
            st.markdown('<h2 class="section-title">COMPARACIÓN PERSONALIZADA</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="gpt-output">{gpt_opinion}</div>', unsafe_allow_html=True)

            st.markdown('<h2 class="section-title">RESULTADO DE LA COMPARACIÓN</h2>', unsafe_allow_html=True)
            
            # Mostrar resultados en tarjetas centradas
            st.markdown(f"""
            <div class="comparison-result" style="display: flex; justify-content: center;">
                <div class="comparison-card offer-card" style="margin: 0 10px;">
                    <h3>OFERTA</h3>
                    <h4>{st.session_state.selected_offer['Nombre']}</h4>
                    <p class="info-trigger">Ver información completa</p>
                    <div class="full-info">
                        <p><strong>Formación:</strong> {st.session_state.selected_offer['Formación']}</p>
                        <p><strong>Conocimientos:</strong> {st.session_state.selected_offer['Conocimientos']}</p>
                        <p><strong>Experiencia:</strong> {st.session_state.selected_offer['Experiencia']}</p>
                        <p><strong>Funciones:</strong> {st.session_state.selected_offer['Funciones']}</p>
                    </div>
                </div>
                <div class="comparison-card" style="flex: 0.5; margin: 0 10px;">
                    <h3>Similitud</h3>
                    <div class="similarity-score" style="color: {'#4CAF50' if similarity > 70 else '#FFA500' if similarity > 50 else '#FF0000'};">
                        {similarity:.2f}%
                    </div>
                </div>
                <div class="comparison-card candidate-card" style="margin: 0 10px;">
                    <h3>CANDIDATURA</h3>
                    <h4>{st.session_state.selected_candidate['Nombre']}</h4>
                    <p class="info-trigger">Ver candidatura completa</p>
                    <div class="full-info">
                        <p><strong>Formación:</strong> {st.session_state.selected_candidate['Formación']}</p>
                        <p><strong>Conocimientos:</strong> {st.session_state.selected_candidate['Conocimientos']}</p>
                        <p><strong>Experiencia:</strong> {st.session_state.selected_candidate['Experiencia']}</p>
                        <p><strong>Idiomas:</strong> {st.session_state.selected_candidate['Idiomas']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

if __name__ == "__main__":
    main()
