import streamlit as st
from openai import OpenAI
import config
import pandas as pd
from nltk.corpus import stopwords
import nltk
from components.comparison import get_gpt_explanation
from components.job_offers import display_job_offers
from components.candidates import display_candidates
from google_sheets import read_sheet
from utills.visualization import display_bar_chart
from streamlit_echarts import st_echarts
from utills.data_processing import calculate_similarity
from streamlit_echarts import st_echarts


# Configuración de la página
st.set_page_config(page_title="NLPMatchJobs", layout="wide")

st.markdown("""
<style>

    .gpt-output {
    
    background-color: #340034 ; /* Un morado similar al de la imagen */
    color: white;
    padding: 2rem;
    margin: 1.5rem 0;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
    
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    .reportview-container {
        background: #99006A
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: #99006A;
    }
    h1, h3 {
        color: #f7efe2;
        text-align: center;
    }

    
    h2 {
        color: #f7efe2;
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
        #stDecoration {display:none;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden !important;}

      .comparison-result {
        background-color: #3b3d0f ;  /* Light blue-gray background */
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


# Descargar stopwords en español
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# ... (other imports and configurations remain the same)

def remove_stop_words(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)
# ... (other imports and configurations remain the same)

def remove_stop_words(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


st.markdown('<h1 class="main-title">COMPARADOR DE OFERTAS Y CANDIDATURAS DE TRABAJO - EINNOVA DEVELOPMENT</h1>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

def main():

    # Inicializar variables de sesión
    if 'selected_offer' not in st.session_state:
        st.session_state.selected_offer = None
    if 'selected_candidate' not in st.session_state:
        st.session_state.selected_candidate = None

    sheet_title = "MyNewSheets"

    try:
        # Cargar datos de ofertas y candidatos
        worksheet_jobs = read_sheet(credentials=config.credentials, range_val='Hoja 1')
        job_offers_data = worksheet_jobs
        
        worksheet_candidates = read_sheet(credentials=config.credentials, range_val='Hoja 2')
        candidates_data = worksheet_candidates
        
        # Mostrar ofertas y candidatos
        display_job_offers(job_offers_data)

        st.markdown("<br><br>", unsafe_allow_html=True)
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
            Si la oferta se ajusta al perfil de la candidatura enseña un número y un correo para poder ponerse en contacto con el candidato, no con la empresa que oferta el trabajo.
            No me tienes que dar un resumen del contenido de la oferta y la candidatura sino una conclusión desarrollada argumentando muy bien si la candidatura se ajusta bien a la oferta.
            Asegurate que cuando haya un punto aparte o este signo ":" haya un salto de linea.
            Quiero que el texto este bien estructurado, con subsecciones, posibles listados, etcétera. No me des en el texto : ### Análisis de la Oferta y la Candidatura. 
            Entre el fin y el comienzo de una subseccion o seccion debe haber una linea horizontal separadora
            Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion = get_gpt_explanation(gpt_opinion_prompt)
            st.markdown('<h2 class="section-title">ENCAJE DEL CANDIDATO CON LA OFERTA 💼', unsafe_allow_html=True)
            st.markdown(f'<div class="gpt-output">{gpt_opinion}</div>', unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.markdown('<h2 class="section-title">DATA SCIENCE EINNOVA 📈</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="section-title">Te explicamos que es el PLN y la similitud textual</h3>', unsafe_allow_html=True)

            gpt_opinion_prompt2 = f"""
             Eres un científico de datos profesional y tienes que explicar de forma resumida y para todos los públicos qué es el procesamiento de lenguaje natural (PLN)
             y cómo podemos comparar la similitud de dos textos mediante herramientas de PLN.

             Además tienes que decir que se va a mostrar la similitud textual entre la oferta y candidatura seleccionada. Debes mencionar brevemente que
             para comparar la similitud de los dos textos, utilizamos técnicas de PLN como la tokenización, la vectorización y el cálculo de la distancia entre vectores,
             las cuales son técnicas que nos permiten cuantificar la similitud entre los textos de manera precisa y objetiva.

             Debes explicar que puede haber casos en los que haya candidatos que presenten un bajo porcentaje de similitud con la oferta pero que se ajustan bien a los requerimientos
             de las ofertas debido a cómo se ha redactado la candidatura y los términos usados.

             Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion2 = get_gpt_explanation(gpt_opinion_prompt2)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f'<div class="gpt-output">{gpt_opinion2}</div>', unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Mostrar resultados en tarjetas centradas
            st.markdown(f"""
            <div class="comparison-result" style="display: flex; justify-content: center;">
                    <h3>HEMOS DETECTADO UN {similarity:.2f}% DE SIMILITUD ENTRE AMBOS TEXTOS</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            gpt_opinion_prompt3 = f"""
             Eres un científico de datos profesional y tienes que sacar conclusiones del porcentaje de similitud textual obtenido entre el texto
             de la oferta y el de la candidatura: {similarity:.2f}. Recuerda evitar sacar conclusiones relacionadas con que el candidato no se ajusta a la oferta, ya que puede haber casos en los que
             haya candidatos que presenten un bajo porcentaje de similitud con la oferta pero que se ajustan bien a los requerimientos de las ofertas debido a cómo se ha redactado la candidatura y los términos usados.

             Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            """
            gpt_opinion3 = get_gpt_explanation(gpt_opinion_prompt3)
            st.markdown(f'<div class="gpt-output">{gpt_opinion3}</div>', unsafe_allow_html=True)

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Incluir la idea del radar
            radar_data = [
                {"name": term, "oferta": offer_score * 100, "candidato": candidate_score * 100}
                for term, (offer_score, candidate_score) in top_terms
            ]

            options = {
                "title": {"text": "Comparación de Términos Clave", "textStyle": {"color": "#2c3e50"}},
                "legend": {"data": ["Oferta", "Candidato"], "textStyle": {"color": "#34495e"}},
                "radar": {
                    "indicator": [{"name": item["name"], "max": 100} for item in radar_data],
                    "splitArea": {"areaStyle": {"color": ["rgba(250,250,250,0.3)", "rgba(200,200,200,0.3)"]}},
                },
                "series": [{
                    "type": "radar",
                    "data": [
                        {
                            "value": [item["oferta"] for item in radar_data],
                            "name": "Oferta",
                            "itemStyle": {"color": "#4CAF50"},
                            "areaStyle": {"color": "rgba(76,175,80,0.3)"}
                        },
                        {
                            "value": [item["candidato"] for item in radar_data],
                            "name": "Candidato",
                            "itemStyle": {"color": "#2196F3"},
                            "areaStyle": {"color": "rgba(33,150,243,0.3)"}
                        }
                    ]
                }]
            }

            st_echarts(options=options, height="500px")

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
            # Tabla de comparación detallada
            
            comparison_df = pd.DataFrame({
                "Término": [term for term, _ in top_terms],
                "Puntuación Oferta": [f"{score*100:.2f}%" for _, (score, _) in top_terms],
                "Puntuación Candidato": [f"{score*100:.2f}%" for _, (_, score) in top_terms],
                "Diferencia": [(offer_score - candidate_score)*100 for _, (offer_score, candidate_score) in top_terms]
            })                    
            def color_difference(val):
                color = 'lightgreen' if val > 0 else 'lightcoral' if val < 0 else 'white'
                return f'background-color: {color}'

            st.table(comparison_df.style
                    .format({'Diferencia': '{:.2f}%'})
                    .applymap(color_difference, subset=['Diferencia'])
                    .set_properties(**{'color': 'black'}, subset=['Término', 'Puntuación Oferta', 'Puntuación Candidato']))

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Generar texto elaborado y descargar en PDF
            st.markdown('<h2 class="section-title">VISIÓN Y CONCLUSIÓN ESTADÍSTICA</h2>', unsafe_allow_html=True)

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

            gpt_opinion_prompt4 = f"""
            Realiza un análisis estadistico y cientifico de datos , completo, profesional y serio sobre los siguientes textos relacionados con una oferta de trabajo
            y una candidatura.
            (texto de la oferta = {st.session_state.selected_offer}) (texto de la candidature = {st.session_state.selected_candidate}).
            Utiliza toda la información obtenida (similitud de los textos= [{similarity:.2f}], términos importantes = [{top_terms}]  y demás cosas que consideres útil)
            para crear un análisis detallado y estadístico sobre ambos textos seleccionados.  Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
            No me des al principio del mensaje esto: ### Análisis Estadístico y Científico de la Oferta de Trabajo y la Candidatura

            """
            gpt_opinion4 = get_gpt_explanation(gpt_opinion_prompt4)
            st.markdown(f'<div class="gpt-output">{gpt_opinion4}</div>', unsafe_allow_html=True)


 

    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

if __name__ == "__main__":
    main()



