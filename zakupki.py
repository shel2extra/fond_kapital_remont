import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
import wget

headres = Headers(os='Windows', browser='chrome')

url = 'https://zakupki.gov.ru//epz/capitalrepairs/card/document.html?reestr-number=224263680812500208'

response = requests.get(url=url, headers=headres.generate())
soup = bs(response.content, 'html.parser')

links = [x for x in soup.find_all('a') if x.text.endswith(('.pdf', '.jpg', '.xlsx', '.rar'))]

for link in links[2:5]:
    wget.download(link['href'])

# for link in tqdm(links[2:5]):
#     name_file = link.text.strip()
#     res_down = requests.get(link['href'], headers=headres.generate(), stream=True)
#     res_down.raise_for_status()
#
#     total_size_in_bytes = int(res_down.headers.get('content-length', 0))
#     block_size = 1024  # 1 КБ
#     progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
#
#     with open(name_file, 'wb+') as file:
#         for data in res_down.iter_content(block_size):
#             progress_bar.update(len(data))
#             file.write(data)



# data = requests.get('https://zakupki.gov.ru/44fz/filestore/public/1.0/download/rd/file.html?uid'
#               '=EC6308C8A755EF11E05334548D0AD381', headers=headres.generate(), stream=True)
# data.raise_for_status()
# with open('data.pdf', 'wb+') as file:
#     file.write(data.content)