from bs4 import BeautifulSoup
from datetime import datetime
import radio, program
import requests
import re

site = 'https://rfm.sapo.pt/'
i = 0

def fds(tabela: list):
    # find a div in tabela with class = "row topSpace"
    dia = []
    mudouDia = 0
    programacao = []
    programa = program.Program()
    
    for row in tabela.find_all('div', class_='row topSpace'):
        a = row.find('li', class_="pTxtRed").find('a')
        img = row.find_all('img')
        info = row.find_all("li", class_="pTxtLightGrey")
        prox = row.find('span')
        if a:
            programa.link = site + a['href']
            programa.title = a.text
        if img:
            programa.img = []
            for i in img:
                programa.img.append(i['src'])

        if info:
            for elem in info:
                elem = elem.text.split('-')
                if len(elem) == 2:
                    programa.start = datetime.strptime(elem[0][:2], '%H').time()
                    if elem[1][1:3] == '24':
                        programa.end = datetime.strptime('00', '%H').time()
                    else:
                        programa.end = datetime.strptime(elem[1][1:3], '%H').time()

        if prox:
            mudouDia = 1
            programacao += dia
            dia = []

        if programa.isComplete():
            if mudouDia == 1:
                programa.details += "DOM"
            else: 
                programa.details += "SAB"
            dia.append(programa)
            programa = program.Program()

    programacao += dia
    return programacao

def trataINFO(info):
    aux = []
    tipo = 0
    match = re.match(r'(.*)(\d{2}:\d{2}) - (\d{2}:\d{2})', info)
    match2 = re.match(r'(\d{2}:\d{2}) - (\d{2}:\d{2})', info)
    if "|" in info:
        info = info.split("|")
        for i in info:
            match = re.match(r'(.*)(\d{2}:\d{2}) - (\d{2}:\d{2})', i)
            aux.append((match.group(1).strip(), match.group(2).strip(), match.group(3).strip()))
        tipo = 1
    elif match:
        aux.append((match.group(1).strip(), match.group(2).strip(), match.group(3).strip()))
        tipo = 2
    elif match2:
        aux.append((match2.group(1).strip(), match2.group(2).strip()))
        tipo = 3
    else:
        aux.append(info)
        tipo = 4

    return aux, tipo



def semana(tabela: list):
    # find a div in tabela with class = "row topSpace"
    dia = []
    mudouDia = 0
    programa = program.Program()
    
    for row in tabela.find_all('div', class_='row topSpace'):
        a = row.find('li', class_="pTxtRed").find('a')
        img = row.find_all('img')
        info = row.find_all("li", class_="pTxtLightGrey")
        prox = row.find('span')
        if a:
            programa.link = site + a['href']
            programa.title = a.text

        if img:
            programa.img = []
            for i in img:
                programa.img.append(i['src'])

        if info:
            for elem in info:
                elem=elem.text
                res, tipo = trataINFO(elem)
                
                if tipo == 1:
                    programa.start = datetime.strptime(res[0][1], '%H:%M').time()
                    if res[0][2] == '24:00':
                        programa.end = datetime.strptime('00:00', '%H:%M').time()
                    else:
                        programa.end = datetime.strptime(res[0][2], '%H:%M').time()

                    programa.details += res[0][0] + " | " + " ".join(res[1])
                elif tipo == 2:
                    if programa.start == None:
                        programa.start = datetime.strptime(res[0][1], '%H:%M').time()
                        if res[0][2] == '24:00':
                            programa.end = datetime.strptime('00:00', '%H:%M').time()
                        else:
                            programa.end = datetime.strptime(res[0][2], '%H:%M').time()

                        programa.details += res[0][0]
                    else:
                        programa.details += " | " + " ".join(res[0])

                elif tipo == 3:
                    programa.start = datetime.strptime(res[0][0], '%H:%M').time()
                    if res[0][1] == '24:00':
                        programa.end = datetime.strptime('00:00', '%H:%M').time()
                    else:
                        programa.end = datetime.strptime(res[0][1], '%H:%M').time() 
                else:
                    programa.details += res[0]                    

        if programa.isComplete():
            dia.append(programa)
            programa = program.Program()
    
    return dia


def rfm():
    url = site + 'programas'
    #dia = '0'
    #data = {'dia': dia, 'randval': 0.1234}
    programacao = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    global i
    i = 0

    programacao = semana(soup.find("div",{"id":"week"}))
    programacao += fds(soup.find("div",{"id":"weekend"}))

    radio_ = radio.Radio('RFM', 'https://images.rfm.sapo.pt/logo_rfm_r6285e5bd.png', site, programacao)
    return radio_
    
rfm()

