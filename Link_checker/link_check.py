import csv
import random

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
headres = Headers(os='Windows', browser='chrome')


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
    return "https://zakupki.gov.ru" + protokol_link

def link_protokol_checker(url, num):
    respone = requests.get(url=url, headers=headres.generate())
    soup = bs(respone.content, 'html.parser')
    try:
        count_request = soup.find('span', text='Количество поданных заявок').find_next()
        print(num, count_request.text)
    except:
        pass


list_links = []
with open('result_links.csv', 'r', encoding='utf-8') as csv_file:
    links = [x for x in csv_file.readlines() if "Отсутсвует" not in x]
    # for link in links[:10]:
    #     link_protokol_checker(link.split(',')[-1])
    for i in range(30):
        ran = random.choice(links)
        link_protokol_checker(ran.split(',')[-1], ran.split(',')[0])
