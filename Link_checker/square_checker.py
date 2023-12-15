import csv
import time
import asyncio, aiohttp
from tqdm.auto import tqdm
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def check_3(num, session, pbar):
    url = 'https://ru.reestrgos.com/api/objects/single'
    payload = f"{{\"number\": \"{num}\"}}"
    try:
        async with session.post(url=url, data=payload) as response:
            square = await response.read()
            square = json.loads(square)['response']['data']['area']
            with open('kadastr_result2.csv', 'a', newline='') as wr_csv:
                writer = csv.writer(wr_csv)
                writer.writerow([num, square])
    except:
        pass
    pbar.update(1)

async def process_batch(nums, session):
    pbar = tqdm(total=len(nums), position=1, leave=False, desc='Sub', ncols=80)
    tasks = []
    for num in nums:
        task = asyncio.create_task(check_3(num, session, pbar))
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
    my_conn = aiohttp.TCPConnector(limit=20)
    headers = {
        'authority': 'ru.reestrgos.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'api-token': 'd41d8cd98f00b204e',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://ru.reestrgos.com',
        'referer': 'https://ru.reestrgos.com/poisk-po-kadastrovomu-nomeru',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-kl-kfa-ajax-request': 'Ajax_Request'
    }
    async with aiohttp.ClientSession(connector=my_conn) as session:
        session.headers.update(headers)
        # TODO: Продолжить выполнение с ________184
        batch_size = 1000  # Установите размер пакета подходящим образом
        for i in tqdm(range(0, len(list_kadastr), batch_size), position=0, desc='ALL', ncols=80, leave=False):
            batch = list_kadastr[i:i + batch_size]
            await process_batch(batch, session)
    time_end = time.time() - time_start
    print(f"Время работы - {time_end:.2f}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
