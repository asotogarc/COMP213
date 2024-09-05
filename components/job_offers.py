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
    .card-link form {
        display: inline-block;
    }
    .card-link input[type="submit"] {
        background-color: rgba(255,255,255,0.2);
        border: none;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .card-link input[type="submit"]:hover {
        background-color: rgba(255,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (offer, col) in enumerate(zip(st.session_state.job_offers, cols)):
        with col:
            is_selected = 'selected_offer' in st.session_state and st.session_state.selected_offer == offer
            card_class = "card"
            
            # Mostrar el nombre de la oferta, la formación y el botón de selección en la tarjeta
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-title">
                    <h3>{offer['Nombre']}</h3>
                    <p>{offer['Formación']}</p>
                    <div class="card-link">
                        <form method="POST">
                            <input type="hidden" name="offer_index" value="{i}">
                            <input type="submit" value="{'(Deseleccionar Oferta)' if is_selected else '(Seleccionar Oferta)'}" name="select_offer">
                        </form>
                    </div>
                </div>
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
    
    # Manejar la selección de oferta
    if st.session_state.get('selected_offer') is None:
        st.session_state.selected_offer = None

    if st.request.method == "POST":
        data = st.experimental_get_query_params()
        if "select_offer" in data:
            offer_index = int(data.get("offer_index", [0])[0])
            if st.session_state.selected_offer == st.session_state.job_offers[offer_index]:
                st.session_state.selected_offer = None
            else:
                st.session_state.selected_offer = st.session_state.job_offers[offer_index]
            st.experimental_rerun()

    # Mostrar la oferta seleccionada y realizar la comparación
    if st.session_state.selected_offer:
        st.write("Oferta seleccionada:")
        st.json(st.session_state.selected_offer)
        # Aquí puedes añadir la lógica para realizar la comparación
        st.write("Comparación de la oferta con el perfil del candidato:")
        # Implementa aquí la lógica de comparación
        st.write("(Aquí se mostraría el resultado de la comparación)")

# Asegúrate de llamar a esta función con los datos adecuados en tu aplicación principal
# display_job_offers(data)
