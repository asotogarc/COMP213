import streamlit as st

def display_candidates(data):
    if 'candidates' not in st.session_state:
        st.session_state.candidates = data.sample(n=min(3, len(data))).to_dict('records')
    
    if 'selected_candidate' not in st.session_state:
        st.session_state.selected_candidate = None

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
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (candidate, col) in enumerate(zip(st.session_state.candidates, cols)):
        with col:
            is_selected = st.session_state.selected_candidate == candidate
            card_class = "card selected" if is_selected else "card"
            
            with st.container():
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="card-title">{candidate['Nombre']}</div>
                    <div class="card-experience">{candidate['Experiencia']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Candidato", key=f"candidate_{i}"):
                    if is_selected:
                        st.session_state.selected_candidate = None
                    else:
                        st.session_state.selected_candidate = candidate
                    st.rerun()

    # No mostramos información adicional del candidato seleccionado
