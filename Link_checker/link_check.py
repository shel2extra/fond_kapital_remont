import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers


def link_checker(num_url):
    url = f'https://zakupki.gov.ru/epz/order/notice/ea615/view/documents.html?regNumber={num_url}'
    respone = requests.get(url=url, headers=headres.generate())
    soup = bs(respone.content, 'html.parser')
    try:
        protokol_link = soup.find('h2', text='Протоколы работы комиссии').find_parent().find('div', class_='section__value '
                                                                                                       'docName').find(
        'a')['href']
    except:
        protokol_link = 'Отсутсвует'
    print(protokol_link)


headres = Headers(os='Windows', browser='chrome')
with open('links.txt', 'r') as file:
    links = [x.replace('\n', '').replace('в„–', '').strip() for x in file.readlines()]
    for link in links[:10]:
        link_checker(link)