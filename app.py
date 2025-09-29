import streamlit as st
import random

st.set_page_config(page_title="Antena Meteorológica IF", page_icon="🌦️")

# Simulação de dados
temperatura = random.randint(20, 35)
umidade = random.randint(40, 90)
vento = random.randint(5, 20)

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
		font-size:28px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Humidade do ar:<br><br><br>
		{temperatura} ºC
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
		font-size:28px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Vel. do Vento:<br><br><br>
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
		font-size:28px;
		font-family:Inria Serif;
        	text-align:center;
        	">
		Humidade do ar:<br><br><br>
		{umidade} "%"
    	</div>
    	""",
   	unsafe_allow_html=True
)



col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", f"{temperatura} °C")
col2.metric("Umidade", f"{umidade} %")
col3.metric("Velocidade do vento", f"{vento} km/h")

# Gráfico exemplo
dados = [random.randint(20, 35) for _ in range(7)]
st.line_chart(dados)