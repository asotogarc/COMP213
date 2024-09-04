import streamlit as st

def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')
    
    n_samples = len(st.session_state.candidates)
    if n_samples == 0:
        st.warning("No hay candidatos para mostrar.")
        return None
    
    st.markdown('<h2>POSTULACIONES</h2>', unsafe_allow_html=True)
    
    # El estilo CSS ya está definido en display_job_offers, no es necesario repetirlo aquí
    
    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):
        with col:
            is_selected = st.session_state.get('selected_candidate') == candidate
            card_class = "card"
            
            # Mostrar el nombre del candidato directamente en la tarjeta
            st.markdown(f"""
            <div class="{card_class}">
                <h3>{candidate['Nombre']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón de selección
            if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Candidato", key=f"candidate_{i}"):
                if is_selected:
                    st.session_state.selected_candidate = None
                else:
                    st.session_state.selected_candidate = candidate
                st.rerun()
            
            with st.expander("Ver Conocimientos"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{candidate['Conocimientos']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Ver Experiencia"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{candidate['Experiencia']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Ver Idiomas"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{candidate['Idiomas']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Ver Ubicación"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{candidate['Localidad']}, {candidate['Provincia']}</p>
                </div>
                """, unsafe_allow_html=True)
