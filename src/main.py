# Request a cada rádio e buscar a programação (por enquanto) e o que está a dar
# Imprimir a programação e o que está a dar
import requests
import cidadefm
import renascenca
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
import urllib.request
import database
from datetime import time
import random

# MODULOS DE RÁDIOS
import megahits
import rfm
import observador
import comercial

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


def centeredImage(img,nome):
    st.markdown(f"""<div style='height: 250px; display: flex; align-items: center;'>
                        <figure>
                            <img src='{img}' style='display: block;margin: auto; width: 60%'>
                        </figure>
                    </div>""", unsafe_allow_html=True)

def show_page(radio):
    "A opção escolhida foi: ["+ radio.name +"](" + radio.link +")"

    _, col2, _ = st.columns(3)
    with col2:
        centeredImage(radio.img, radio.name)

    for program in radio.schedule:
        if len(program.day) > 1:
            program.day = program.day[0] + " - " + program.day[-1]
        else:
            program.day = program.day[0]
        with st.expander("__"+program.title + "__ | " + program.day + " (" + program.start + " - " + program.end + ")"):
            program.details
            program.link

            colms = st.columns(len(program.img) + 2)

            idx = 1

            if isinstance(program.img, list):
                for img in program.img:
                    with colms[idx]:
                        idx += 1
                        st.image(img,width=200)
            else:
                with colms[idx]:
                    idx += 1
                    st.image(program.img, width=200)

def show_day(radios,programas):
    if len(radios) == 0:
        st.error("Não foram encontradas rádios com a programação disponível para o dia de hoje")
        return
    
    cols = st.columns(len(radios))
    i = 0                

    for i in range(len(radios)):
        with cols[i]:
            centeredImage(radios[i]["img"], radios[i]["name"])

            for programa in programas:
                if programa["radio"] == radios[i]["name"]:
                    
                    if len(programa["day"]) > 1:
                        programa["day"] = programa["day"][0] + " - " + programa["day"][-1]
                    else:
                        programa["day"] = programa["day"][0]

                    with st.expander("__"+programa["title"] + "__ | " + programa["day"] + " (" + programa["start"] + " - " + programa["end"] + ")"):
                        programa["details"]
                        programa["link"]

                        colms = st.columns(len(programa["img"]) + 2)

                        idx = 1

                        if isinstance(programa["img"], list):
                            for img in programa["img"]:
                                with colms[idx]:
                                    idx += 1
                                    st.image(img, width=200)
                        else:
                            with colms[idx]:
                                idx += 1
                                st.image(programa["img"], width=200)

st.set_page_config(
    page_title="Guia de Rádios",
    page_icon=":radio:",
    layout="wide",
    initial_sidebar_state="expanded",
)


bd = database.BD()

# carregar BD
if bd.checkUpdate():
    with st.spinner('A carregar...'):
        # MEGA HITS
        radio = megahits.megahits({"user-agent": random.choice(user_agent_list)})
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

        # RFM
        radio = rfm.rfm({"user-agent": random.choice(user_agent_list)})
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

        # OBSERVADOR
        radio = observador.observador({"user-agent": random.choice(user_agent_list)})
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

        # COMERCIAL
        radio = comercial.comercial({"user-agent": random.choice(user_agent_list)})
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())


        # CIDADE FM
        radio = cidadefm.cidade({"user-agent": random.choice(user_agent_list)})
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

        # RENASCENÇA
        radio = renascenca.renascenca({"user-agent": random.choice(user_agent_list)})
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

filtro = st.selectbox(
    'Como pretende filtrar a programação?',
    ("",'Por dia', 'Por rádio'))

radio = None

if filtro == "Por rádio":
    opcao = st.selectbox(
    'Qual rádio?',
    ("",'RFM', 'Mega Hits', 'Observador','Rádio Comercial', 'Cidade FM', 'Renascença'))

    if opcao == "RFM":
        radio = bd.getEntry("RFM")
        show_page(radio)

    elif opcao == "Mega Hits":
        radio = bd.getEntry("Mega Hits")
        show_page(radio)
    
    elif opcao == "Observador":
        radio = bd.getEntry("Observador")
        show_page(radio)
    
    elif opcao == "Rádio Comercial":
        radio = bd.getEntry("Rádio Comercial")
        show_page(radio)

    elif opcao == "Cidade FM":
        radio = bd.getEntry("Cidade FM")
        show_page(radio)
    
    elif opcao == "Renascença":
        radio = bd.getEntry("Renascença")
        show_page(radio)

elif filtro == "Por dia":
    dia = st.selectbox(
    'Qual dia?',
    ("",'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'))
    tradutor = {
        "Segunda": "SEG",
        "Terça": "TER",
        "Quarta": "QUA",
        "Quinta": "QUI",
        "Sexta": "SEX",
        "Sábado": "SAB",
        "Domingo": "DOM"
    }

    if dia != "":
        # filtrar desde uma hora
        hora = st.slider('A partir de que horas?', time(0), time(23), time(0))
        hora = hora.strftime("%H:%M")
        radios,programas = bd.getDayHour(tradutor[dia], hora)
        "A opção escolhida foi: "+ dia +" a partir das " + hora
        show_day(radios,programas)