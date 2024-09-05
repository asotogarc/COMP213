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
        cursor: pointer;
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
    </style>
    """, unsafe_allow_html=True)
    
    # Crear contenedores para las ofertas
    offer_containers = st.columns(n_samples)
    
    for i, (offer, container) in enumerate(zip(st.session_state.job_offers, offer_containers)):
        with container:
            is_selected = st.session_state.selected_offer == offer
            card_class = "card selected" if is_selected else "card"
            
            # Usamos un único botón para seleccionar/deseleccionar
            if st.button("Seleccionar" if not is_selected else "Deseleccionar", key=f"offer_{i}"):
                st.session_state.selected_offer = offer if not is_selected else None
                st.rerun()
            
            # La tarjeta ahora es solo visual
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-title">{offer['Nombre']}</div>
                <div class="card-formation">{offer['Formación']} <a href="{offer['URL']}" target="_blank" class="card-link">🔗</a></div>
            </div>
            """, unsafe_allow_html=True)

    # Mostrar la oferta seleccionada
    if st.session_state.selected_offer:
        st.write("Oferta seleccionada:", st.session_state.selected_offer['Nombre'])
