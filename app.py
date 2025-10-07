import streamlit as st
import random
import datetime
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=120000, key="update")
URL = "https://antena-metereologica-default-rtdb.firebaseio.com/leituras.json"
agora = datetime.datetime.now().strftime("%H:%M")
st.set_page_config(page_title="Antena Meteorológica IF", page_icon="🌦️")

def get_last_data():
    try:
        r = requests.get(URL, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data:
                # Pega a última leitura (última chave no dicionário)
                last_key = list(data.keys())[-1]
                last_data = data[last_key]

                temperatura = last_data.get("Temperatura", 0)
                hora = last_data.get("Time", "N/A")

                return temperatura, hora
        else:
            st.error(f"Erro HTTP: {r.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com o Firebase: {e}")
    return 0, 0, 0, "N/A"
temperatura, hora= get_last_data()

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

st.markdown(
    """
    <p style="
        color:#000000;
        font-size:28px;
        font-family:Inria Serif;
        text-align:center;
        font-weight:bold;
    ">
    🌦️Antena Meteorológica IFSP-Salto
    </p>
     """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
with col1:
	st.markdown(
    	f"""
    	<div style="
        	width:165px;
        	height:120px;
        	background-color:#D0FFCC;
       		border-radius:4px;
		margin-left:0px;
        	margin-right:auto; 
		margin-top:40px;
 		display:flex;
        	align-items:flex-start;
        	justify-content:center;  
		color:#D00003;
		font-size:24px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Temperatura:<br><br>
		{temperatura} °C
    	</div>
    	""",
   	unsafe_allow_html=True
)
with col2:
	st.markdown(
    	f"""
    	<div style="
        	width:165px;
        	height:120px;
        	background-color:#D0FFCC;
       		border-radius:4px;
		margin-left:0px;
        	margin-right:auto; 
		margin-top:40px;
 		display:flex;
        	align-items:flex-start;
        	justify-content:center;  
		color:#D00003;
		font-size:24px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Vel. do Vento:<br><br>
		{vento} km/h
    	</div>
    	""",
   	unsafe_allow_html=True
)

with col3:
	st.markdown(
    	f"""
    	<div style="
        	width:165px;
        	height:120px;
        	background-color:#D0FFCC;
       		border-radius:4px;
		margin-left:0px;
        	margin-right:auto; 
		margin-top:40px;
 		display:flex;
        	align-items:flex-start;
        	justify-content:center;  
		color:#D00003;
		font-size:24px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Humidade do ar:<br><br>
		{umidade} %
    	</div>
    	""",
   	unsafe_allow_html=True
)


dados = [random.randint(20, 35) for _ in range(7)]
st.line_chart(dados)
