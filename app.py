import streamlit as st
import random

st.set_page_config(page_title="Antena Meteorológica", page_icon="🌦️")
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌦️ Antena Meteorológica Online")

# Simulação de dados
temperatura = random.randint(20, 35)
umidade = random.randint(40, 90)
vento = random.randint(5, 20)

col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", f"{temperatura} °C")
col2.metric("Umidade", f"{umidade} %")
col3.metric("Velocidade do vento", f"{vento} km/h")

# Gráfico exemplo
dados = [random.randint(20, 35) for _ in range(7)]
st.line_chart(dados)
