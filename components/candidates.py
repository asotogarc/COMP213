import streamlit as st

def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')
    
    if 'selected_candidate' not in st.session_state:
        st.session_state.selected_candidate = None

    def toggle_candidate(candidate):
        if st.session_state.selected_candidate == candidate:
            st.session_state.selected_candidate = None
        else:
            st.session_state.selected_candidate = candidate

    n_samples = len(st.session_state.candidates)
    if n_samples == 0:
        st.warning("No hay candidatos para mostrar.")
        return None
    
    st.markdown('<h2>POSTULACIONES</h2>', unsafe_allow_html=True)
    
    # Estilo CSS actualizado
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
        transition: all 0.3s ease;
    }
    .card.selected {
        border: 5px solid #28a745;
        transform: scale(1.05);
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-experience {
        font-size: 14px;
        margin-bottom: 10px;
    }
    .stButton > button {
        width: 100%;
        background-color: rgba(255,255,255,0.2);
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        transition: background-color 0.3s, transform 0.3s;
    }
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):
        with col:
            is_selected = st.session_state.selected_candidate == candidate
            card_class = "card selected" if is_selected else "card"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-title">{candidate['Nombre']}</div>
                <div class="card-experience">{candidate['Experiencia']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            button_text = "Deseleccionar candidato" if is_selected else "Seleccionar candidato"
            if st.button(button_text, key=f"candidate_{i}", on_click=toggle_candidate, args=(candidate,)):
                pass  # La lógica de selección se maneja en la función de callback
