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
        padding: 15px;
        margin: 15px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: #556dac;
    }
    .card-title {
        height: 80px;  /* Aumentada la altura para más espacio */
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        background-color: #556dac;  /* Cambiado el color de fondo */
        border-radius: 5px;
        padding: 10px;
    }
    .card-title h3 {
        margin: 0;
        text-align: center;
        font-size: 18px;  /* Aumentado el tamaño de la fuente */
        line-height: 1.3;
        font-weight: bold;
        color: #fff;  /* Cambiado el color del texto a blanco */
    }
    .card-content {
        height: 70px;
        overflow-y: auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #556dac;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
    .card-content p {
        margin: 0;
        text-align: center;
        font-size: 14px;
    }
    .stButton > button {
        width: 100%;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (offer, col) in enumerate(zip(st.session_state.job_offers, cols)):
        with col:
            is_selected = 'selected_offer' in st.session_state and st.session_state.selected_offer == offer
            card_class = "card"
            
            # Mostrar el nombre de la oferta directamente en la tarjeta con altura fija
            st.markdown(f"""
                <div class="card-title">
                    <h3>{offer['Nombre']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón de selección espaciado y debajo de los expanders
            if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Oferta", key=f"offer_{i}"):
                if is_selected:
                    st.session_state.selected_offer = None
                else:
                    st.session_state.selected_offer = offer
                st.rerun()
            
            with st.expander("Formación necesaria"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{offer['Formación']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Conocimientos requeridos"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{offer['Conocimientos']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Ubicación donde se realiza el trabajo"):
                st.markdown(f"""
                <div class="card-content">
                    <p>{offer['Localidad']}</p>
                </div>
                """, unsafe_allow_html=True)
