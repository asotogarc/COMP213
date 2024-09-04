import streamlit as st
from openai import OpenAI
import config
import pandas as pd
from nltk.corpus import stopwords
import nltk
from components.comparison import get_gpt_explanation
from components.job_offers import display_job_offers
from google_sheets import read_sheet
from utills.visualization import display_bar_chart
from streamlit_echarts import st_echarts
from utills.data_processing import calculate_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity





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

def calculate_term_weights(text, top_n=5):
    vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    weights = tfidf_matrix.toarray()[0]
    term_weights = sorted(zip(feature_names, weights), key=lambda x: x[1], reverse=True)[:top_n]
    return dict(term_weights)

def create_spider_chart(offer_terms, candidate_terms):
    terms = list(set(offer_terms.keys()) | set(candidate_terms.keys()))
    offer_values = [offer_terms.get(term, 0) for term in terms]
    candidate_values = [candidate_terms.get(term, 0) for term in terms]
    
    option = {
        "title": {"text": "Top 5 Terms Comparison"},
        "radar": {
            "indicator": [{"name": term, "max": 1} for term in terms]
        },
        "series": [{
            "type": "radar",
            "data": [
                {
                    "value": offer_values,
                    "name": "Job Offer"
                },
                {
                    "value": candidate_values,
                    "name": "Candidate"
                }
            ]
        }]
    }
    return option

def create_comparative_table(offer_terms, candidate_terms):
    df = pd.DataFrame({
        "Term": offer_terms.keys(),
        "Offer Weight": offer_terms.values(),
        "Candidate Weight": [candidate_terms.get(term, 0) for term in offer_terms.keys()],
    })
    df["Difference"] = df["Offer Weight"] - df["Candidate Weight"]
    df = df.sort_values("Difference", ascending=False)
    return df

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
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.markdown('<h2 class="section-title">DATA SCIENCE EINNOVA</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="section-title">¿Qué es el PLN y la similitud textual?</h3>', unsafe_allow_html=True)

            gpt_opinion_prompt2 = f"""

             Eres un científico de datos profesional y tienes que  explicar de forma resumida y para todos los públicos qué es el procesamiento de lenguaje natural (PLN)
             y cómo podemos comparar la similitud de dos textos mediante herramientas de PLN.

             Además tienes que decir que se va a mostrar la similitud textual entre la oferta y candidatura seleccionada. Debes mencionar brvemente que
             para comparar la similitud de los dos textos, utilizamos técnicas de PLN como la tokenización, la vectorización y el cálculo de la distancia entre vectores.
             las cuales son técnicas que nos permiten cuantificar la similitud entre los textos de manera precisa y objetiva.

             Debes explicar que puede haber casos en los que haya candidatos que presenten un bajo porcentaje de similitud con la oferta pero que se ajustan bien a los requerimientos
             de las ofertas debido a como se ha redactado la candidatura y los terminos usados



            
             Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion2 = get_gpt_explanation(gpt_opinion_prompt2)

            st.markdown(f'<div class="gpt-output">{gpt_opinion2}</div>', unsafe_allow_html=True)

            
            # Mostrar resultados en tarjetas centradas
            st.markdown(f"""
            <div class="comparison-result" style="display: flex; justify-content: center;">
                <div class="comparison-card offer-card" style="margin: 0 10px;">
                    
                    <h3>{similarity:.2f}</h3>
                    <p class="info-trigger">Ver información completa</p>
                </div>

              
            </div>
            """, unsafe_allow_html=True)

            gpt_opinion_prompt3 = f"""

             Eres un científico de datos profesional y tienes que sacar conclusiones del porcentaje de similitud textual obtenido entre el texto
             de la oferta y el de la candidatura: {similarity}. Recuerda evitar sacar conclusiones relacionadas con que el candidaot no se ajusta a la oferta, ya que puede haber casos en los que
                haya candidatos que presenten un bajo porcentaje de similitud con la oferta pero que se ajustan bien a los requerimientos de las ofertas debido a como se ha redactado la candidatura y los terminos usados



            
             Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion3 = get_gpt_explanation(gpt_opinion_prompt3)
            st.markdown(f'<div class="gpt-output">{gpt_opinion3}</div>', unsafe_allow_html=True)



            offer_terms = calculate_term_weights(st.session_state.selected_offer)
            candidate_terms = calculate_term_weights(st.session_state.selected_candidate)

            # Create and display spider chart
            st.markdown('<h3 class="section-title">Spider Chart: Top 5 Terms Comparison</h3>', unsafe_allow_html=True)
            spider_chart_option = create_spider_chart(offer_terms, candidate_terms)
            st_echarts(options=spider_chart_option, height="500px")


    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

if __name__ == "__main__":
    main()
