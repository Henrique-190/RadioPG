# Request a cada rádio e buscar a programação (por enquanto) e o que está a dar
# Imprimir a programação e o que está a dar


import requests
import megahits
import rfm
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
import urllib.request
  
st.set_page_config(
    page_title="Guia de Rádios",
    page_icon=":radio:",
    layout="centered",
    initial_sidebar_state="expanded",
)

option = st.selectbox(
    'Qual é a programação que pretende visualizar?',
    ('RFM', 'MegaHits'))

radio = None

with st.spinner('A carregar...'):
    if option == "RFM":
        radio = rfm.rfm()    

    elif option == "MegaHits":
        radio = megahits.megahits()
    
"A opção escolhida foi: ["+ radio.name +"](" + radio.link +")"

_, col2, _ = st.columns(3)
with col2:
    st.image(radio.img, caption=radio.name)

for program in radio.schedule:
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