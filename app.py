import streamlit as st
import random
import datetime
from flask import Flask, request
import threading

# ============== SERVIDOR FLASK (para receber dados do ESP32) ==============
app_flask = Flask(__name__)

# Dicionário global com os últimos dados recebidos
dados_esp32 = {"temperatura": 0, "umidade": 0, "vento": 0, "hora": ""}

@app_flask.route('/update', methods=['POST'])
def update():
    global dados_esp32
    data = request.get_json()
    if data:
        dados_esp32.update(data)
        print("📡 Dados recebidos:", dados_esp32)
        return "OK", 200
    return "Erro no formato", 400

def run_flask():
    app_flask.run(host="0.0.0.0", port=5000)

# Inicia o servidor Flask em uma thread separada
threading.Thread(target=run_flask, daemon=True).start()

# ============== INTERFACE STREAMLIT ==============
st.set_page_config(page_title="Antena Meteorológica IF", page_icon="🌦️")

st.markdown(
    """
    <style>
    .stApp { background-color: white; }
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

# Mostra os dados do ESP32
st.subheader("📊 Dados em tempo real do ESP32")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌡️ Temperatura", f"{dados_esp32['temperatura']} °C")
with col2:
    st.metric("💨 Vento", f"{dados_esp32['vento']} km/h")
with col3:
    st.metric("💧 Umidade", f"{dados_esp32['umidade']} %")

st.write(f"⏱️ Atualizado às: {dados_esp32['hora']}")