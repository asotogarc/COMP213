import streamlit as st

def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')
    
    n_samples = len(st.session_state.candidates)
    if n_samples == 0:
        st.warning("No hay candidatos para mostrar.")
        return None
    
    st.markdown('<h2>POSTULACIONES</h2>', unsafe_allow_html=True)
    
    # Estilo CSS personalizado con animación y ajuste automático de altura
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .card {
        border: 1px solid #ddd;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card-title {
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        background-color: #007bff;
        border-radius: 5px 5px 0 0;
    }
    .card-title h3 {
        margin: 0;
        text-align: center;
        font-size: 18px;
        line-height: 1.3;
        color: white;
        padding: 10px;
    }
    .card-content {
        overflow-y: auto;
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        padding: 10px;
    }
    .card-content p {
        margin: 0;
        text-align: left;
        animation: fadeIn 0.5s ease-in;
    }
    .stExpander {
        border: none !important;
        box-shadow: none !important;
    }
    .streamlit-expanderHeader {
        border-radius: 5px !important;
        background-color: #f0f2f6 !important;
    }
    .streamlit-expanderContent {
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):
        with col:
            is_selected = st.session_state.get('selected_candidate') == candidate
            card_class = "card"
            
            # Mostrar el nombre del candidato directamente en la tarjeta
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-title">
                    <h3>{candidate['Nombre']}</h3>
                </div>
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
