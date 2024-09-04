import streamlit as st
from openai import OpenAI
import config
import pandas as pd
from nltk.corpus import stopwords
import nltk
from components.comparison import get_gpt_explanation
from utills.data_processing import calculate_similarity
from components.job_offers import display_job_offers
from google_sheets import read_sheet 
from google_sheets import write_sheets
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
    st.title("EINNOVA AI -- COMPARADOR DE CANDIDATURAS Y OFERTAS DE TRABAJO")

    # Inicializar variables de sesión
    if 'selected_offer' not in st.session_state:
        st.session_state.selected_offer = None
    if 'selected_candidate' not in st.session_state:
        st.session_state.selected_candidate = None

    sheet_title = "MyNewSheets"

    try:
        # Cargar datos de ofertas y candidatos
        worksheet_jobs = read_sheets(sheet_title, "Hoja 1")
        job_offers_data = worksheet_jobs
        
        worksheet_candidates = read_sheets(sheet_title, "Hoja 2")
        candidates_data = worksheet_candidates
        
        # Mostrar ofertas y candidatos
        display_job_offers(job_offers_data)
        display_candidates(candidates_data)
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Botón de comparación centrado y más grande
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
          
        </div>
        """, unsafe_allow_html=True)

        # Botón oculto de Streamlit para manejar la lógica
        if st.button("Realizar Comparación", key="compare_button"):
            if st.session_state.selected_offer and st.session_state.selected_candidate:
                similarity, top_terms = calculate_similarity(st.session_state.selected_offer, st.session_state.selected_candidate)

                                # Opinión personalizada del GPT
                gpt_opinion_prompt = f"""
                Analiza el texto de la oferta:
                {st.session_state.selected_offer}
                
                Y el texto de la candidatura:
                {st.session_state.selected_candidate}
                
                Basándonos en la información de la oferta {st.session_state.selected_offer} y en el de la candidatura {st.session_state.selected_candidate}, opinamos si la oferta se ajusta al perfil del candidato.
                Si la la oferta  se ajusta al perfil de la candidatura enseña un numero y un correo para poder ponerse en contacto con el candidato.
                No me tienes que dar un resumen del contenido de la oferta y la cnadidatura si no una conclusion desarrollado argumentando muy bien si la candidatura se ajusta bien a la oferta
                Después de nuestra opinión, mencionamos que mostraremos los resultados del análisis del procesamiento del lenguaje natural de ambos textos.
                Debes explicar sencillamente y brevemente que puede haber candidatos que se ajustan bien a un perfil pero que la comparación del texto de su candidatura con el de la oferta puede presentar un  bajo porcentaje de similitud
                Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
                
                """
                gpt_opinion = get_gpt_explanation(gpt_opinion_prompt)
                st.markdown('<h2 class="section-title">Recomendación Personalizada</h2>', unsafe_allow_html=True)
                st.markdown(f'<div class="gpt-output">{gpt_opinion}</div>', unsafe_allow_html=True)

        
                st.markdown('<h2 class="section-title">RESULTADO DE LA COMPARACIÓN</h2>', unsafe_allow_html=True)
                
                # Mostrar resultados en tarjetas
                st.markdown(f"""
                <div class="comparison-result">
                    <div class="comparison-card offer-card">
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
                    <div class="comparison-card" style="flex: 0.5;">
                        <h3>Similitud</h3>
                        <div class="similarity-score" style="color: {'#4CAF50' if similarity > 70 else '#FFA500' if similarity > 50 else '#FF0000'};">
                            {similarity:.2f}%
                        </div>
                    </div>
                    <div class="comparison-card candidate-card">
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

                # Explicación detallada del porcentaje de similitud
                similarity_explanation_prompt = f"""
                Explica de forma detallada pero comprensible para cualquier persona el porcentaje de similitud del {similarity:.2f}% 
                obtenido entre la candidatura y la oferta. La explicación debe ser profesional y técnica, pero a la vez fácil de entender.
                Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
                """
                similarity_explanation = get_gpt_explanation(similarity_explanation_prompt)

                # Análisis detallado
                st.subheader("Análisis Detallado")

                # Gráfico de radar
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

                # Gráfico de barras comparativo
                offer_scores = [item["oferta"] for item in radar_data]
                candidate_scores = [item["candidato"] for item in radar_data]
                terms = [item["name"] for item in radar_data]
                display_bar_chart(offer_scores, candidate_scores, terms)

                # Tabla de comparación detallada
                st.markdown('<h2 class="section-title">COMPARACIÓN DETALLADA DE TÉRMINOS</h2>', unsafe_allow_html=True)
                comparison_df = pd.DataFrame({
                    "Término": [term for term, _ in top_terms],
                    "Puntuación Oferta": [f"{score*100:.2f}%" for _, (score, _) in top_terms],
                    "Puntuación Candidato": [f"{score*100:.2f}%" for _, (_, score) in top_terms],
                    "Diferencia": [(offer_score - candidate_score)*100 for _, (offer_score, candidate_score) in top_terms]
                })                    
                def color_difference(val):
                    color = 'green' if val > 0 else 'red' if val < 0 else 'white'
                    return f'background-color: {color}'

                st.table(comparison_df.style
                        .format({'Diferencia': '{:.2f}%'})
                        .applymap(color_difference, subset=['Diferencia'])
                        .set_properties(**{'color': 'black'}, subset=['Término', 'Puntuación Oferta', 'Puntuación Candidato']))

                # Explicación de la comparación de términos clave
                terms_comparison_prompt = f"""
                Analiza y explica de forma detallada pero comprensible las conclusiones de la comparación de términos clave 
                entre la oferta y el candidato. Utiliza la siguiente información:
                {comparison_df.to_string()}
                La explicación debe ser profesional y técnica, pero a la vez fácil de entender para cualquier persona.
                Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
                """
                terms_comparison_explanation = get_gpt_explanation(terms_comparison_prompt)
                st.markdown('<h2 class="section-title">ANÁLISIS DE COMPARACIÓN DE TÉRMINOS CLAVE</h2>', unsafe_allow_html=True)
                st.markdown(f'<div class="gpt-output">{terms_comparison_explanation}</div>', unsafe_allow_html=True)


                # Áreas de mejora
                st.markdown('<h2 class="section-title">Áreas de Mejora para el Candidato</h2>', unsafe_allow_html=True)
                st.markdown('<div class="section-content">', unsafe_allow_html=True)
                improvements = [term for term, (offer_score, candidate_score) in top_terms if offer_score > candidate_score]
                if improvements:
                    improvement_prompt = f"""
                    Basándonos en las siguientes áreas de mejora para el candidato: {', '.join(improvements[:5])},
                    proporcionamos recomendaciones específicas y fáciles de entender para mejorar en estas áreas.
                    Incluimos sugerencias de cursos, videos, libros u otros recursos que puedan ayudar al candidato a mejorar.
                    La explicación debe ser motivadora y orientada al desarrollo profesional.
                    Usamos la primera persona del plural y evitamos respuestas robóticas o frases como "¡Claro!" o "¡Vamos a ello!".
                    """
                    improvement_explanation = get_gpt_explanation(improvement_prompt)
                    st.markdown(f'<div class="gpt-output">{improvement_explanation}</div>', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px;">
                        <p style="color: black;">El candidato cumple o excede todas las áreas requeridas por la oferta. ¡Excelente trabajo!</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Recomendación de leer el análisis



 
            else:
                st.markdown("""
                <div style="background-color: #fff3e0; padding: 10px; border-radius: 5px;">
                    <p style="color: black;">Por favor, seleccione tanto una oferta como un candidato antes de comparar.</p>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    main()
