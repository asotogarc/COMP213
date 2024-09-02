# Importamos las librerias necesarias
import plotly.graph_objects as go
import streamlit as st

def display_bar_chart(offer_scores, candidate_scores, terms):
    fig = go.Figure(data=[
        go.Bar(name='Oferta', x=terms, y=offer_scores, marker_color='#4CAF50'),
        go.Bar(name='Candidato', x=terms, y=candidate_scores, marker_color='#2196F3')
    ])
    fig.update_layout(
        title='Comparación de Términos Clave',
        xaxis_title='Términos',
        yaxis_title='Puntuación',
        barmode='group',
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='#F0EFF0',
        font=dict(color="black"),
        
        xaxis=dict(title=dict(font=dict(color="black")), tickfont=dict(color="black")),
        yaxis=dict(title=dict(font=dict(color="black")), tickfont=dict(color="black"))
    )
    st.plotly_chart(fig, use_container_width=True)
