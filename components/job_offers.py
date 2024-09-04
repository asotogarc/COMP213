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
    for i, (offer, col) in enumerate(zip(st.session_state.job_offers, cols)):
        with col:
            is_selected = 'selected_offer' in st.session_state and st.session_state.selected_offer == offer
            card_class = "card" + (" selected" if is_selected else "")
            
            with st.expander("Ver Nombre Oferta"):
                st.markdown(f"""
                <div class="{card_class}">
                    <h3>Nombre</h3>
                    <p>{offer['Nombre']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown(f"""
                <div class="{card_class}">
                    <h3>Funciones</h3>
                    <p>{offer['Funciones']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botón de selección espaciado y debajo de los expanders
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Oferta", key=f"offer_{i}"):
                    if is_selected:
                        st.session_state.selected_offer = None
                    else:
                        st.session_state.selected_offer = offer
                    st.rerun()
                
                # Usar un expander de Streamlit para las funciones
                with st.expander("Ver Formación"):
                    st.markdown(f"""
                    <div class="{card_class}">
                        <h3>Formación</h3>
                        <p>{offer['Formación']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.expander("Ver Funciones"):
                    st.markdown(f"""
                    <div class="{card_class}">
                        <h3>Funciones</h3>
                        <p>{offer['Funciones']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Expander para los conocimientos
                with st.expander("Ver Conocimientos"):
                    st.markdown(f"""
                    <div class="{card_class}">
                        <h3>Conocimientos</h3>
                        <p>{offer['Conocimientos']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Expander para la localidad
                with st.expander("Ver Localidad"):
                    st.markdown(f"""
                    <div class="{card_class}">
                        <h3>Localidad</h3>
                        <p>{offer['Localidad'], offer['Provincia']}</p>
                    </div>
                    """, unsafe_allow_html=True)
