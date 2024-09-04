# Importamos las librerias necesarias
import streamlit as st

def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')

    n_samples = len(st.session_state.candidates)
    if n_samples == 0:
        st.warning("No hay candidatos para mostrar.")
        return None

    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):
        with col:
            # Menú desplegable con el nombre del candidato
            selected_name = st.selectbox(f"Seleccionar Candidato {i+1}", [candidate['Nombre']], key=f"selectbox_{i}")

            # Verificar si el candidato está seleccionado
            is_selected = st.session_state.get('selected_candidate') == candidate

            # Botón centrado
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Candidato", key=f"candidate_{i}"):
                    if is_selected:
                        st.session_state.selected_candidate = None
                    else:
                        st.session_state.selected_candidate = candidate
                    st.rerun()

            # Expander para los conocimientos
            with st.expander("Ver Conocimientos"):
                st.markdown(f"""
                    {candidate['Conocimientos']}
                """, unsafe_allow_html=True)

            # Expander para la experiencia
            with st.expander("Ver Experiencia"):
                st.markdown(f"""
                    {candidate['Experiencia']}
                """, unsafe_allow_html=True)

            # Expander para los idiomas
            with st.expander("Ver Idiomas"):
                st.markdown(f"""
                    {candidate['Idiomas']}
                """, unsafe_allow_html=True)

            # Expander para la ubicación
            with st.expander("Ver Ubicación"):
                st.markdown(f"""
                    {candidate['Localidad']}, {candidate['Provincia']}
                """, unsafe_allow_html=True)
