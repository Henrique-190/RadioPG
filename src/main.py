# Request a cada rádio e buscar a programação (por enquanto) e o que está a dar
# Imprimir a programação e o que está a dar
import requests
import megahits
import rfm
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
import urllib.request
import database
from datetime import time

# img_to_bytes and img_to_html inspired from https://pmbaumgartner.github.io/streamlitopedia/sizing-and-images.html


def centeredImage(img,nome):
    st.markdown("<figure>", unsafe_allow_html=True)
    st.markdown("<img src='{}' style='display: block;margin-left: auto;margin-right: auto; height: 150px'>".format(img), unsafe_allow_html=True)
    st.markdown("<figcaption style='text-align: center;'>{}</figcaption>".format(nome), unsafe_allow_html=True)
    st.markdown("</figure>", unsafe_allow_html=True)

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
                        st.image(img)
            else:
                with colms[idx]:
                    idx += 1
                    st.image(program.img)

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
                                    st.image(img)
                        else:
                            with colms[idx]:
                                idx += 1
                                st.image(programa["img"])

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
        radio = megahits.megahits()
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

        # RFM
        radio = rfm.rfm()
        bd.insert_radio(radio.name, radio.img, radio.link, radio.scheduleToJson())

filtro = st.selectbox(
    'Como pretende filtrar a programação?',
    ("",'Por dia', 'Por rádio'))

radio = None

if filtro == "Por rádio":
    opcao = st.selectbox(
    'Qual rádio?',
    ("",'RFM', 'Mega Hits'))

    if opcao == "RFM":
        radio = bd.getEntry("RFM")
        show_page(radio)

    elif opcao == "Mega Hits":
        radio = bd.getEntry("Mega Hits")
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
