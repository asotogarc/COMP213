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
        border-radius: 0;
        padding: 10px;
        margin: 10px;
        background-color: #007bff;
        color: white;
        text-align: center;
        transition: border 0.3s ease;
    }
    .card.selected {
        border: 5px solid #28a745;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-formation {
        font-size: 14px;
        margin-bottom: 10px;
    }
    .card-link {
        color: white;
        text-decoration: none;
    }
    .card-link:hover {
        text-decoration: underline;
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
    
    # Crear contenedores para las ofertas
    offer_containers = st.columns(n_samples)
    
    for i, (offer, container) in enumerate(zip(st.session_state.job_offers, offer_containers)):
        with container:
            is_selected = st.session_state.selected_offer == offer
            card_class = "card selected" if is_selected else "card"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-title">{offer['Nombre']}</div>
                <div class="card-formation">{offer['Formación']} <a href="{offer['URL']}" target="_blank" class="card-link">🔗</a></div>
            </div>
            """, unsafe_allow_html=True)
            
            button_text = "Deseleccionar" if is_selected else "Seleccionar oferta"
            if st.button(button_text, key=f"offer_{i}"):
                if is_selected:
                    st.session_state.selected_offer = None
                else:
                    st.session_state.selected_offer = offer
                st.rerun()
