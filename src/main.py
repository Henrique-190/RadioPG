# Request a cada rádio e buscar a programação (por enquanto) e o que está a dar
# Imprimir a programação e o que está a dar
import requests
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
import cidadefm
import renascenca


user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

st.set_page_config(
    page_title="Guia de Rádios",
    page_icon=":radio:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("<h3 style='text-align: center; color: grey;'>Como pretende filtrar a programação?</h3>", unsafe_allow_html=True)

cb1, cb2 = st.columns(2)
with cb1:
    b1 = st.button('Dia', 'dia',use_container_width=True)
with cb2:
    b2 = st.button('Rádio', 'radio',use_container_width=True)

if b1:
    st.session_state['filter'] = "Por dia"
elif b2:
    st.session_state['radio'] = "Por rádio"

if "filter" not in st.session_state:
    st.session_state['filter'] = None

if "hora" not in st.session_state:
    st.session_state['hora'] = "00:00"

if "dia" not in st.session_state:
    st.session_state['dia'] = "SEG"

def centeredImage(img,nome):
    st.markdown(f"""<div style='height: 250px; display: flex; align-items: center;'>
                        <figure>
                            <img src='{img}' style='display: block;margin: auto; width: 60%'>
                        </figure>
                    </div>""", unsafe_allow_html=True)

def show_page(radio):
    _, col2, _ = st.columns(3)
    with col2:
        centeredImage(radio.img, radio.name)

    for program in radio.schedule:
        if len(program.day) > 1:
            program.day = program.day[0] + " - " + program.day[-1]
        else:
            program.day = program.day[0]
        with st.expander("__"+program.title + "__ | " + program.day + " (" + program.start + " - " + program.end + ")"):
            if len(program.img) == 1:
                col1, col2 = st.columns([0.3,1])
                with col1:
                    st.image(program.img[0], width=200)
                with col2:
                    program.details if program.details != None else ""
                    if program.link != None and program.link != "":
                        "[Visite](" + program.link + ")"
            else:
                program.details if program.details != None else ""
                if program.link != None and program.link != "":
                    "[Visite](" + program.link + ")"
                if len(program.img) > 0:
                    colms = st.columns(len(program.img) + 2)
                    idx = 1

                    for img in program.img:
                        with colms[idx]:
                            idx += 1
                            st.image(img, width=200)

def show_day(ans):
   
    radio, programas = ans
    if len(radio) == 0:
        st.error("Não foram encontradas rádios com a programação disponível para o dia de hoje")
        return

    cols = st.columns(len(radio))
    i = 0                

    for i in range(len(radio)):
        with cols[i]:
            centeredImage(radio[i]["img"], radio[i]["name"])

            for programa in programas:
                if programa["radio"] == radio[i]["name"]:
                    
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


radio = None

if st.session_state['filter'] == "Por rádio":
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['RFM', 'Mega Hits', 'Observador', 'Rádio Comercial', 'Cidade FM', 'Rádio Renascença'])

    with tab1:
        radio = bd.getEntry("RFM")
        show_page(radio)
    
    with tab2:
        radio = bd.getEntry("Mega Hits")
        show_page(radio)
    
    with tab3:
        radio = bd.getEntry("Observador")
        show_page(radio)
    
    with tab4:
        radio = bd.getEntry("Rádio Comercial")
        show_page(radio)
    
    with tab5:
        radio = bd.getEntry("Cidade FM")
        show_page(radio)
    
    with tab6:
        radio = bd.getEntry("Rádio Renascença")
        show_page(radio)
    

elif st.session_state['filter'] == "Por dia":
    hora = st.slider('A partir de que horas?', time(0), time(23), time(0))
    hora = hora.strftime("%H:%M")
    st.session_state['hora'] = hora
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])
    with tab1:
        show_day(bd.getDayHour("SEG", hora))
    with tab2:
        show_day(bd.getDayHour("TER", hora))
    with tab3:
        show_day(bd.getDayHour("QUA", hora))
    with tab4:
        show_day(bd.getDayHour("QUI", hora))
    with tab5:
        show_day(bd.getDayHour("SEX", hora))
    with tab6:
        show_day(bd.getDayHour("SAB", hora))
    with tab7:
        show_day(bd.getDayHour("DOM", hora))
        