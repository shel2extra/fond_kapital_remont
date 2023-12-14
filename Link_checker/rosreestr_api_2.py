import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import aiohttp
import asyncio

# url = "https://lk.rosreestr.ru/account-back/on"
num = "26:12:022704:346"
payload = f"""{{"filterType": "cadastral", "cadNumbers": ["{num}"]}}"""
headers = {
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
# def check_us():
  # response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  # return response

async def check():
  my_con = aiohttp.TCPConnector(limit=25, ssl=False)
  async with aiohttp.ClientSession(connector=my_con) as session:
    session.headers.update(headers)
    urls = 'https://jsonip.com/'
    proxys = "http://88.201.217.203:80"
    async with session.post(url=urls, proxy=proxys) as response_2:
      ip = await response_2.json()
      print(ip['ip'])
      # square = await response_2.json()
      # print(square['elements'][0]['area'])

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(check())

  # print(check_us())
# print(response['elements'][0]['area'])
