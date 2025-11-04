import streamlit as st
import random
import datetime
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=120000, key="update")
URL = "https://antena-metereologica-default-rtdb.firebaseio.com/leituras.json"
data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
st.set_page_config(page_title="Antena Meteorológica IF", page_icon="🌦️")

def get_last_data():
    try:
        r = requests.get(URL, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data:
                last_key = list(data.keys())[-1]
                last_data = data[last_key]

                temperatura = last_data.get("Temperatura", 0)
                umidade = last_data.get("Umidade", 0)
                vento = last_data.get("Vento", 0)
                hora = last_data.get("Time", "N/A")  # <--- default seguro

                return temperatura, umidade, vento, hora
        else:
            st.error(f"Erro HTTP: {r.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com o Firebase: {e}")

    # Se deu erro ou não houver dados, devolve valores padrão
    return 0, 0, 0, "N/A"

temperatura, umidade, vento, hora = get_last_data()

st.markdown(
    """
    <style>
    /* Remove padding do topo do app */
    .css-1d391kg {  /* container principal */
        padding-top: 0rem;
    }

    /* Remove espaçamento padrão do Streamlit entre blocos */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
	margin-top:0px;
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

dias = [
        (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d/%m")

    for i in range(7)]
dias.reverse()
if (datetime.datetime.now().strftime("%d") = dias[i]
	dias[i] = "Agora")

selection = st.pills(" ", dias, selection_mode="single")

col4, col5, col6 = st.columns(3)

with col4:
	st.markdown(
    	f"""
    	<div style="
		margin-left:0px;
        	margin-right:auto; 
		margin-top:10px;
 		display:flex;
        	align-items:flex-start;
        	justify-content:center;  
		color:black;
		font-size:24px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		{hora}
    	</div>
    	""",
   	unsafe_allow_html=True
)

with col5:
	st.markdown(
    	f"""
    	<div style="
		margin-top:10px;
		margin-left:0px;
        	margin-right:auto; 
 		display:flex;
        	align-items:flex-start;
        	justify-content:center;  
		color:black;
		font-size:24px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		{data_atual}
    	</div>
    	""",
   	unsafe_allow_html=True
)

with col6:
	st.markdown(
    	f"""
    	<div style="
		margin-top:10px;
		margin-left:0px;
        	margin-right:auto; 
 		display:flex;
        	align-items:flex-start;
        	justify-content:center;  
		color:black;
		font-size:24px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Salto/SP
    	</div>
    	""",
   	unsafe_allow_html=True
)
