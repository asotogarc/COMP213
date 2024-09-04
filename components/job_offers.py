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
            
            
            with st.expander("Ver Nombre Oferta"):
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





def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')
    
    n_samples = len(st.session_state.candidates)
    if n_samples == 0:
        st.warning("No hay candidatos para mostrar.")
        return None

    st.markdown('<h2 class="section-title">CANDIDATOS</h2>', unsafe_allow_html=True)
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
        color: #000000;
        margin-bottom: 10px;
    }
    .select-button {
        margin-top: 5px;
        padding-top: 50px;
        border-top: 1px solid #e0e0e0;
        float: right; /* Mueve el botón a la derecha */
        /* float: left;  Mueve el botón a la izquierda */
    }
    .expander-content p, .expander-content h3 {
        color: #000000; /* Color negro */
    }
    .card p, .card h3 {
        color: #000000; /* Color negro */
    }
    .st-expander .st-expanderHeader {
        color: #000000 !important; /* Color negro */
    }
    .st-expander .st-expanderHeader div {
        color: #000000 !important; /* Color negro */
    }
    </style>
    """, unsafe_allow_html=True)
    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):

        with col:
            is_selected = 'selected_candidate' in st.session_state and st.session_state.selected_candidate == candidate
            card_class = "card" + (" selected" if is_selected else "")
            st.markdown(f"""
            <div class="{card_class}">
                <h2>{candidate['Nombre']}</h2>
            </div>
            """, unsafe_allow_html=True)
     
            </div>
            """, unsafe_allow_html=True)
            # Botón centrado
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Candidato", key=f"candidate_{i}"):
                    if is_selected:
                        st.session_state.selected_candidate = None
                    else:
                        st.session_state.selected_candidate = candidate
                    st.rerun()

# Expander para los conocimientos
            with st.expander("Ver Formación"):
                st.markdown(f"""
                <div class="expander-content">
                    <h3>Formación</h3>
                    <p>{candidate['Formación']}</p>
                </div>
                """, unsafe_allow_html=True)


            with st.expander("Ver Idiomas"):
                                st.markdown(f"""
                                <div class="expander-content">
                                    <h3>Formación</h3>
                                    <p>{candidate['Idiomas']}</p>
                                </div>
                                """, unsafe_allow_html=True)


            # Expander para los conocimientos
            with st.expander("Ver Conocimientos"):
                st.markdown(f"""
                <div class="expander-content">
                    <h3>Conocimientos</h3>
                    <p>{candidate['Conocimientos']}</p>
                </div>
                """, unsafe_allow_html=True)

            # Expander para la experiencia
            with st.expander("Ver Experiencia"):
                st.markdown(f"""
                <div class="expander-content">
                    <h3>Experiencia</h3>
                    <p>{candidate['Experiencia']}</p>
                </div>
                """, unsafe_allow_html=True)

                    # Expander para la experiencia
            with st.expander("Ver Ubicación"):
                st.markdown(f"""
                <div class="expander-content">
                    <h3>Ubicación</h3>
                    <p>{candidate['Localidad'],candidate['Provincia']}</p>
                </div>
                """, unsafe_allow_html=True)
