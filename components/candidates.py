import streamlit as st

def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')

    n_samples = len(st.session_state.candidates)
    if n_samples == 0:
        st.warning("No hay candidatos para mostrar.")
        return None


    st.markdown('<h2>POSTULACIONES</h2>', unsafe_allow_html=True)

    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):
        with col:
            # Expander para los conocimientos
            # Verificar si el candidato está seleccionado
            is_selected = st.session_state.get('selected_candidate') == candidate



            with st.expander("Ver Nombre"):
                st.markdown(f"""{candidate['Nombre']}""", unsafe_allow_html=True)
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
                st.markdown(f"""{candidate['Conocimientos']}""", unsafe_allow_html=True)

            # Expander para la experiencia
            with st.expander("Ver Experiencia"):
                st.markdown(f"""{candidate['Experiencia']}""", unsafe_allow_html=True)

            # Expander para los idiomas
            with st.expander("Ver Idiomas"):
                st.markdown(f"""{candidate['Idiomas']}""", unsafe_allow_html=True)

            # Expander para la ubicación
            with st.expander("Ver Ubicación"):
                st.markdown(f"""{candidate['Localidad']}, {candidate['Provincia']}""", unsafe_allow_html=True)
