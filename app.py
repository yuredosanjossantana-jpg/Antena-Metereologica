import streamlit as st
import random
import datetime
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
from datetime import timedelta


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
                vento=vento*3.6
                vento = round(vento,1)
                hora = last_data.get("Hora", "N/A")  # <--- default seguro
                data = last_data.get("Data", "N/A")  # <--- default seguro
                return temperatura, umidade, vento, hora, data
        else:
            st.error(f"Erro HTTP: {r.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com o Firebase: {e}")

    # Se deu erro ou não houver dados, devolve valores padrão
    return 0, 0, 0, "N/A","N/A"

temperatura, umidade, vento, hora, data = get_last_data()

eh = (umidade/100) * 6.105 * \
        (2.71828 ** ((17.27 * temperatura) / (237.7 + temperatura)))    
ta = (
        temperatura
        + 0.33 * eh
        - 0.70 * vento
        - 4.00
    )
ta = round(ta,1)

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
    🌦️Estação Meteorológica IFSP-Salto
    </p>
     """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
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
		Umidade do ar:<br><br>
		{umidade}%
    	</div>
    	""",
   	unsafe_allow_html=True
)
with col4:
	st.markdown(
    	f"""
    	<div style="
        	width:190px;
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
		Sensação Termica:<br><br>
		{ta} °C
    	</div>
    	""",
   	unsafe_allow_html=True
)

def carregar_dados():
    try:
        r = requests.get(URL, timeout=10)

        if r.status_code == 200:
            data = r.json()

            registros = []

            for _, value in data.items():

                registros.append({
                    "Data": value.get("Data"),
                    "Hora": value.get("Hora"),
                    "Temperatura": value.get("Temperatura"),
                    "Umidade": value.get("Umidade"),
                    "Vento": value.get("Vento", 0) * 3.6
                })

            return pd.DataFrame(registros)

    except Exception as e:
        st.error(e)

    return pd.DataFrame()

df = carregar_dados()
df["datetime"] = pd.to_datetime(
    df["Data"] + " " + df["Hora"],
    dayfirst=True,
    errors="coerce"
)

# Remove datas inválidas
df = df.dropna(subset=["datetime"])

# Data de hoje
data_teste = datetime.date(2026, 5, 29)

df_hoje = df[
    df["datetime"].dt.date == data_teste
]
df_media = (
    df_hoje
    .groupby("hora")
    .agg({
        "Temperatura": "mean",
        "Umidade": "mean",
        "Vento": "mean"
    })
    .reset_index()
)
st.write("Registros de hoje:", len(df_hoje))
st.write(df_hoje.head())
st.write(df_media)

horas = [f"{i:02d}:00" for i in range(24)]

# Temperaturas aleatórias
temperaturas = [
    random.uniform(18, 32)
    for _ in range(24)
]

# Dados que aparecerão no tooltip
umidades = [
    random.uniform(50, 95)
    for _ in range(24)
]

ventos = [
    random.uniform(0, 15)
    for _ in range(24)
]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=horas,
        y=temperaturas,
        mode="lines+markers",

        customdata=list(
            zip(umidades, ventos)
        ),

        hovertemplate=
        "<b>%{x}</b><br>" +
        "🌡️ Temperatura: %{y:.1f} °C<br>" +
        "💧 Umidade: %{customdata[0]:.1f}%<br>" +
        "💨 Vento: %{customdata[1]:.1f} km/h<br>" +
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="Hora",
    yaxis_title="Temperatura (°C)",font=dict(size=22),
    template="plotly_white",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)
dias = [
        (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d/%m")

    for i in range(7)]
dias.reverse()
for i in range(len(dias)):
    if datetime.datetime.now().strftime("%d/%m") == dias[i]:
        dias[i] = "Agora"
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
		{data}
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
