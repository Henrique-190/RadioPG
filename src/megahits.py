from bs4 import BeautifulSoup
from datetime import datetime
import radio, program
import requests

site = 'https://megahits.sapo.pt/'
i = 0
def diario(tabela: list):
    programas = []
    for row in tabela:
        titulo = row.find('a')['title']
        link = site + row.find('a')['href']
        horas = row.find('td','pg-gr-li-dt1').text #0007 - 00 é a hora inicial e 07 é a hora final
        try:
            inicial = datetime.strptime(horas[:2], '%H')
            final = datetime.strptime(horas[2:], '%H')
        except ValueError:
            inicial = None
            final = None
        detalhes = row.find('td', class_='pg-gr-li-tx2').text
        imagem = row.find('a').find('img', class_='img-fluid')['src']
        
        programa = program.Program(titulo, link, inicial, final, imagem, detalhes)
        programas.append(programa)
    return programas


def megahits():
    url = site + 'ajax/programacao/getgrelha.aspx'
    dia = '0'
    data = {'dia': dia, 'randval': 0.1234}
    programacao = []

    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.text,"html.parser")
    global i
    i = 0
    while i < 5:
        i += 1
        programacao.append(diario(soup.find_all('li', class_='pg-gr-li1')))

    while i < 7:
        dia = str(i)
        data['dia'] = dia
        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text,"html.parser")
        programacao.append(diario(soup.find_all('li', class_='pg-gr-li1')))
        i += 1

    radio_ = radio.Radio('Mega Hits', 'https://megahits.sapo.pt/img/logo.png', site, programacao)
    return radio_
    

print(megahits())


