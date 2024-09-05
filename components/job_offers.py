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
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card-title {
        min-height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #007bff;
        border-radius: 5px 5px 0 0;
        padding: 10px;
    }
    .card-title h3 {
        margin: 0 0 10px 0;
        text-align: center;
        font-size: 18px;
        line-height: 1.3;
        color: white;
    }
    .card-title p {
        margin: 0 0 10px 0;
        text-align: center;
        font-size: 14px;
        line-height: 1.2;
        color: white;
    }
    .card-content {
        height: 60px;
        overflow-y: auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .card-content p {
        margin: 0;
        text-align: center;
    }
    .card-link {
        text-align: center;
        margin-top: 10px;
    }
    .stButton > button {
        width: 100%;
        background-color: rgba(255,255,255,0.2);
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (offer, col) in enumerate(zip(st.session_state.job_offers, cols)):
        with col:
            is_selected = 'selected_offer' in st.session_state and st.session_state.selected_offer == offer
            card_class = "card"
            
            # Mostrar el nombre de la oferta y la formación en la tarjeta
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-title">
                    <h3>{offer['Nombre']}</h3>
                    <p>{offer['Formación']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón de selección dentro de la tarjeta
            if st.button(f"{'Deseleccionar' if is_selected else '(Seleccionar Oferta)'}", key=f"offer_{i}"):
                if is_selected:
                    st.session_state.selected_offer = None
                else:
                    st.session_state.selected_offer = offer
                st.rerun()
            
            # Mostrar el enlace a la oferta
            st.markdown(f"[Ver oferta completa]({offer['URL']})", unsafe_allow_html=True)

    # Si hay una oferta seleccionada, mostrar información adicional
    if 'selected_offer' in st.session_state and st.session_state.selected_offer:
        st.markdown("## Oferta Seleccionada")
        st.write(st.session_state.selected_offer)
