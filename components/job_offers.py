import streamlit as st

def display_job_offers(data):
    if 'job_offers' not in st.session_state:
        st.session_state.job_offers = data.sample(n=min(3, len(data))).to_dict('records')
    
    n_samples = len(st.session_state.job_offers)
    if n_samples == 0:
        st.warning("No hay ofertas de trabajo para mostrar.")
        return None
    
    st.markdown('

OFERTAS DE TRABAJO

', unsafe_allow_html=True)
    
    # Estilo CSS personalizado
    st.markdown("""
    
    """, unsafe_allow_html=True)
    
    cols = st.columns(n_samples)
    for i, (offer, col) in enumerate(zip(st.session_state.job_offers, cols)):
        with col:
            
            is_selected = 'selected_offer' in st.session_state and st.session_state.selected_offer == offer
            card_class = "card" + (" selected" if is_selected else "")
            
            with st.expander("Ver Nombre Oferta"):
                st.markdown(f"""
                

Funciones


                

{offer['Nombre']}

 


                """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown(f"""
                
              
                """, unsafe_allow_html=True)
                
                # Eliminar la línea horizontal encima del botón de selección
                # st.markdown('

', unsafe_allow_html=True)
                
                if st.button(f"{'Deseleccionar' if is_selected else 'Seleccionar'} Oferta", key=f"offer_{i}"):
                    if is_selected:
                        st.session_state.selected_offer = None
                    else:
                        st.session_state.selected_offer = offer
                    st.rerun()
                st.markdown('

', unsafe_allow_html=True)
                
                # Usar un expander de Streamlit para las funciones
                with st.expander("Ver Formación"):
                    st.markdown(f"""
                    

Funciones


                    

{offer['Formación']}


                    """, unsafe_allow_html=True)
                
                with st.expander("Ver Funciones"):
                    st.markdown(f"""
                    

Funciones


                    

{offer['Funciones']}


                    """, unsafe_allow_html=True)
                
                # Expander para los conocimientos
                with st.expander("Ver Conocimientos"):
                    st.markdown(f"""
                    

Conocimientos


                    

{offer['Conocimientos']}


                    """, unsafe_allow_html=True)
                
                # Expander para los conocimientos
                with st.expander("Ver Localidad"):
                    st.markdown(f"""
                    

Conocimientos


                    

{offer['Localidad']}


                    """, unsafe_allow_html=True)
