import streamlit as st

def display_job_offers(data):
    if 'job_offers' not in st.session_state:
        st.session_state.job_offers = data.sample(n=min(3, len(data))).to_dict('records')
    
    if 'selected_offer' not in st.session_state:
        st.session_state.selected_offer = None

    n_samples = len(st.session_state.job_offers)
    if n_samples == 0:
        st.warning("No hay ofertas de trabajo para mostrar.")
        return None
    
    st.markdown('<h2>OFERTAS DE TRABAJO</h2>', unsafe_allow_html=True)
    
    # Estilo CSS personalizado
    st.markdown("""
    <style>
    .card {
        border: 2px solid #ddd;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
    }
    .card.selected {
        border-color: #28a745;
    }
    .card-title {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 5px 5px 0 0;
        text-align: center;
    }
    .card-title h3 {
        margin: 0 0 10px 0;
        font-size: 18px;
        line-height: 1.3;
    }
    .card-title p {
        margin: 0;
        font-size: 14px;
        line-height: 1.2;
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
            is_selected = st.session_state.selected_offer == offer
            card_class = "card selected" if is_selected else "card"
            
            with st.container():
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="card-title">
                        <h3>{offer['Nombre']}</h3>
                        <p>{offer['Formación']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar Oferta'}", key=f"offer_{i}"):
                    if is_selected:
                        st.session_state.selected_offer = None
                    else:
                        st.session_state.selected_offer = offer
                    st.experimental_rerun()
                
                st.markdown(f"[Ver oferta completa]({offer['URL']})", unsafe_allow_html=True)

    # No mostramos información adicional de la oferta seleccionada
