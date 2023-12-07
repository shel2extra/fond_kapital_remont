import csv
import time

from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as BS
from fake_headers import Headers
from selenium import webdriver


# options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# # free proxy server URL
# proxy_server_url = "202.131.65.110:80"
# options.add_argument(f'--proxy-server={proxy_server_url}')
# driver = webdriver.Chrome(options=options)
# driver.get('https://2ip.ru')
# # driver.get(url='https://xn--80aq1a.xn--p1aee.xn--p1ai/overhaul/overhaul/contractor?inn=010300243466&name=ИП%20Величко')
# time.sleep(50)


headers = Headers(os='Windows', browser='chrome')

def get_contactor():
    all_data = []
    for page in range(1, 8):
        url = f'https://xn--80aq1a.xn--p1aee.xn--p1ai/overhaul/overhaul/contractors?sf=2214158&inn=&contractorName=&page' \
              f'={page}&limit=32&order=ASC&sortName=inn_position'
        response = requests.get(url=url, headers=headers.generate())
        soup = BS(response.content, 'html.parser')
        table = soup.find('table', class_='table-spacing').find('tbody').find_all('tr')
        for tab in table:
            url = 'https://xn--80aq1a.xn--p1aee.xn--p1ai'+tab.find('a')['href'].replace(' ', '%20')
            name = tab.find('a').text
            inn = tab.find_all('td', class_='dark-text')[0].text
            count_work = tab.find_all('td', class_='dark-text')[1].text

            all_data.append([url, name, inn, count_work])
        print(f'{page} -- Done!')

    with open('all_data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_data)
all_data = []

def get_info_about_contactor(url_contactor, name):
    pages = True
    page = 1
    while pages:
        response = requests.get(url_contactor+f'&page={page}&limit=32&order=ASC&sort=address', headers=headers.generate())
        soup = BS(response.content, 'html.parser')
        try:
            table = soup.find('table', class_='table-spacing').find('tbody').find_all('tr')
            if int(len(table)) == 0:
                pages = False
                continue
            else:
                for tab in table:
                    addres = tab.find('a').text
                    vid_rabot = tab.find_all('td')[1].text
                    price_1 = tab.find_all('td')[2].text
                    price_2 = tab.find_all('td')[3].text
                    price_3 = tab.find_all('td')[4].text
                    date = tab.find_all('td')[5].text
                    all_data.append([name, addres, vid_rabot, price_1, price_2, price_3, date])
            time.sleep(5)
        except:
            pass
        print(f'Обработана страница - {page}')
        page += 1



with open('all_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    for one_row in tqdm(list(reader)[196:]):
        if int(one_row[-1]) > 0:
            get_info_about_contactor(url_contactor=one_row[0], name=one_row[1])
        print(f'Обработан {one_row[1]}')

        with open('data_contactor.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(all_data)
        all_data.clear()