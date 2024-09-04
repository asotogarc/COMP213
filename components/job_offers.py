import streamlit as st

def display_job_offers(data):
    if 'job_offers' not in st.session_state:
        st.session_state.job_offers = data.sample(n=min(3, len(data))).to_dict('records')
    
    n_samples = len(st.session_state.job_offers)
    if n_samples == 0:
        st.warning("No hay ofertas de trabajo para mostrar.")
        return None
    
    st.markdown('<h2 class="section-title">OFERTAS DE TRABAJO</h2>', unsafe_allow_html=True)
    
    # Estilo CSS personalizado
    st.markdown("""
    <style>
    .offer-details h3 {
        font-size: 1.2em;
        color: #4A4A4A;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    .offer-details p {
        font-size: 1em;
        color: #6A6A6A;
        margin-bottom: 10px;
    }
    .select-button {
        margin-top: 20px;
        padding-top: 10px;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (offer, col) in enumerate(zip(st.session_state.job_offers, cols)):
        with col:



            
            is_selected = 'selected_offer' in st.session_state and st.session_state.selected_offer == offer
            card_class = "card" + (" selected" if is_selected else "")
            
            
            with st.expander("Ver Formación"):
                    st.markdown(f"""
                    <h3>Funciones</h3>
                    <p><h2><a href="{offer['URL']}" target="_blank" class="offer-link::after">{offer['Nombre']}</a></h2> </p>
                    """, unsafe_allow_html=True)

            
            
            with st.container():
                st.markdown(f"""
                
              
                """, unsafe_allow_html=True)
                 # Botón de selección espaciado y debajo de los expanders
                st.markdown('<div class="select-button">', unsafe_allow_html=True)
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Oferta", key=f"offer_{i}"):
                    if is_selected:
                        st.session_state.selected_offer = None
                    else:
                        st.session_state.selected_offer = offer
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                # Usar un expander de Streamlit para las funciones

                with st.expander("Ver Formación"):
                    st.markdown(f"""
                    <h3>Funciones</h3>
                    <p>{offer['Formación']}</p>
                    """, unsafe_allow_html=True)
                
                with st.expander("Ver Funciones"):
                    st.markdown(f"""
                    <h3>Funciones</h3>
                    <p>{offer['Funciones']}</p>
                    """, unsafe_allow_html=True)
                
                # Expander para los conocimientos
                with st.expander("Ver Conocimientos"):
                    st.markdown(f"""
                    <h3>Conocimientos</h3>
                    <p>{offer['Conocimientos']}</p>
                    """, unsafe_allow_html=True)
                
                # Expander para los conocimientos
                with st.expander("Ver Localidad"):
                    st.markdown(f"""
                    <h3>Conocimientos</h3>
                    <p>{offer['Localidad']}</p>
                    """, unsafe_allow_html=True)
               
