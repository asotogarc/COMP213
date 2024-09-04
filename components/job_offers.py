import streamlit as st

def display_job_offers(data):
    if 'job_offers' not in st.session_state:
        st.session_state.job_offers = data.sample(n=min(3, len(data))).to_dict('records')
    
    n_samples = len(st.session_state.job_offers)
    if n_samples == 0:
        st.warning("No hay ofertas de trabajo para mostrar.")
        return None
    
    st.markdown('<h2>OFERTAS DE TRABAJO</h2>', unsafe_allow_html=True)
    
    # Estilo CSS personalizado
    st.markdown("""
    <style>
    .card {
        border: 1px solid #ddd;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
    }
    .selected {
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
        for i, (candidate, col) in enumerate(zip(st.session_state.offer, cols)):
        with col:
            # Verificar si el candidato está seleccionado
            is_selected = st.session_state.get('selected_candidate') == candidate

            # Botón centrado
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Oferta", key=f"offer_{i}"):
                    if is_selected:
                        st.session_state.selected_offer = None
                    else:
                        st.session_state.selected_offer = candidate
                    st.rerun()
            
            # Expander para los conocimientos
            with st.expander("Ver Conocimientos"):
                st.markdown(f"""
                
                
                {offer['Experiencia']}
                """, unsafe_allow_html=True)

           
