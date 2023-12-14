import csv
from bs4 import BeautifulSoup as bs
import time
import asyncio, aiohttp
from tqdm.auto import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def check_by_rosreestr(num, session, pbar):
    url = "https://lk.rosreestr.ru/account-back/on"
    payload = f"""{{"filterType": "cadastral", "cadNumbers": ["{num}"]}}"""
    async with session.post(url=url, data=payload) as response:
        print(num, response)



async def check_square(num, session, pbar):
    async with session.get(url=f'https://kadastrmap.ru/reestr/{num}/') as response:
        try:
            soup = bs(await response.read(), 'lxml')
            square = soup.find('td', class_='td_info', text=' Общая площадь: ').find_next().text.strip()
            with open('kadastr_result.csv', 'a', newline='') as wr_csv:
                writer = csv.writer(wr_csv)
                writer.writerow([num, square])
        except:
            pass
        pbar.update(1)
        return

async def process_batch(nums, session):
    pbar = tqdm(total=len(nums), position=1, leave=False, desc='Sub', ncols=80)
    tasks = []
    for num in nums:
        num = num.replace(':', '-')
        task = asyncio.create_task(check_by_rosreestr(num, session, pbar))
        # task = asyncio.create_task(check_square(num, session, pbar))
        tasks.append(task)
    await asyncio.gather(*tasks)
    return


async def main():
    time_start = time.time()
    list_kadastr = []
    with open(r'C:\Users\User\Desktop\РАБОТА АПСК\2023\13. Фонд капитального ремонта\kadasrt_map.csv', 'r',
              encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter='|')
        next(reader)
        for row in reader:
            list_kadastr.append(row[1])
    tasks = []
    my_conn = aiohttp.TCPConnector(limit=25, verify_ssl=False)
    headers_2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'AUTH_TOKEN=71d78327-9656-5857-75f3-3c02115624bb; hazelcast.sessionId=HZ5B716AE1C2854C648AB4CB80B5A7DE8F; TOMCAT_SESSIONID=4A46325E468DF1E8C81B2F080BF0139A; AUTH_TOKEN=71d78327-9656-5857-75f3-3c02115624bb; _ga=GA1.2.1475506204.1701847619; _gid=GA1.2.1960318063.1702542515; _ga_78LLLS27C6=GS1.1.1702542514.3.1.1702542572.2.0.0; uid=CoHkfGV69tqpP+3BFH5SAg==; session-cookie=17a0b2efec9f869404a1995fbeb261f5c8d7d928a863586ba4104a767b2b043edb084ab4c1964ebf99c4c69f3b4940ba; HOME_URL=https://lk.rosreestr.ru/login?redirect=%2F; AUTH_TOKEN=71d78327-9656-5857-75f3-3c02115624bb; LK_PROFILE_ID=729483693; LK_ROLE=PERSON; PC_USER_WAS_AUTHORIZED=1002773943; AUTH_TOKEN=71d78327-9656-5857-75f3-3c02115624bb; TOMCAT_SESSIONID=E3216EEA92EFA22DC30ACB210AAAC4C4; hazelcast.sessionId=HZ0CF7330870134B8EADD0CFEF6297560C; session-cookie=17a0b355afe8357e04a1995fbeb261f5a69f9ad4beeec0fa41b2bed49501195aea58e262c2bd24ca6bbe0e9d733a7b65; uid=CoHkfGV6+I+pP+3CB7flAg==',
        'DNT': '1',
        'Origin': 'https://lk.rosreestr.ru',
        'Pragma': 'no-cache',
        'Referer': 'https://lk.rosreestr.ru/eservices/real-estate-objects-online',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-KL-kfa-Ajax-Request': 'Ajax_Request',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    async with aiohttp.ClientSession(connector=my_conn) as session:
        session.headers.update(headers_2)
        batch_size = 10  # Установите размер пакета подходящим образом
        for i in tqdm(range(0, len(list_kadastr), batch_size), position=0, desc='ALL', ncols=80, leave=False):
            batch = list_kadastr[i:i + batch_size]
            await process_batch(batch, session)
    time_end = time.time() - time_start
    print(f"Время работы - {time_end:.2f}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
