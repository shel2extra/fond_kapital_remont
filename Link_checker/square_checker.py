import csv
from fake_headers import Headers
from bs4 import BeautifulSoup as bs
import time
import asyncio, aiohttp
from tqdm.auto import tqdm

headers = Headers(os='Windows', browser='chrome')


async def def_check_by_rosreestr():
    pass


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
        task = asyncio.create_task(check_square(num, session, pbar))
        tasks.append(task)
    await asyncio.gather(*tasks)
    return


async def main():
    time_start = time.time()
    list_kadastr = []
    with open(r'C:\Users\User\Desktop\РАБОТА АПСК\2023\13. Фонд капитального ремонта\kadasrt_map.csv', 'r',
              encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter='|')
        for row in reader:
            list_kadastr.append(row[1])
    tasks = []
    my_conn = aiohttp.TCPConnector(limit=25)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        session.headers.update(headers.generate())
        batch_size = 1000  # Установите размер пакета подходящим образом
        for i in tqdm(range(0, len(list_kadastr), batch_size), position=0, desc='ALL', ncols=80, leave=False):
            batch = list_kadastr[i:i + batch_size]
            await process_batch(batch, session)
    time_end = time.time() - time_start
    print(f"Время работы - {time_end:.2f}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
