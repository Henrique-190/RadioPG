from bs4 import BeautifulSoup
import requests
def megahits():
    r = requests.get('https://megahits.sapo.pt/programacao')
    soup = BeautifulSoup(r.text,"html.parser")
    print(soup.find('div', class_='pg-live1').text)
    print(soup.find('img', {'class':['card-img-top', 'img-fluid']})['src'])
    print(soup.find('div', class_='mega-card-title').text)
    print(soup.find('div', class_='mega-card-subtitle').text)

    tabela = soup.find('table', class_='pg-gr-box1')
    programas = []
    
    for row in tabela.find_all('tr'):
        horas = row.find('td', class_='pg-gr-li-dt1').text
        imagem = row.find('td', class_='pg-gr-li-img1').text
        print(row.find('td', class_='pg-gr-box1-artist').text)
        print(row.find('td', class_='pg-gr-box1-genre').text)
        print(row.find('td', class_='pg-gr-box1-duration').text)
        print(row.find('td', class_='pg-gr-box1-views').text)

megahits()