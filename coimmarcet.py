'''
TODO:
2.MUltiprocessing
2.1 data visualization
3.Tg - bot


'''

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from sys import platform
import getpass
import json
from datetime import datetime
from time import sleep
from te import API_KEY
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
  'start': '1',#getting info starting from first crypto
  'limit': '20',
  'convert': 'USD'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}
time_for_sleep = input('Update rate (in sec.) : ')#response time
try:
    int(time_for_sleep)
except ValueError as v:
    print(v)

path = input('path (leave blank for standard path - Desktop):')

platf = platform[:3].lower()#name of user platform
username = getpass.getuser()#OS account username


def get_info(data):
    for i in data['data']:
        nameCrypto = i['name']
        symbolCrypto = i['symbol']
        price = round(float(i['quote']['USD']['price']), 4)
        date = datetime.strftime(datetime.now(), "%H:%M %d.%m.%Y")
        market_cap = round(i['quote']['USD']['market_cap'], 4)
        important_inf = ({'name': nameCrypto,
                              'symbol': symbolCrypto,
                              'price': str(price)+' $',
                              'date': date,
                              'market_cap': str(market_cap)+' $'})
        writer(important_inf) #Recording information for each crypt in the cycle 


def writer(data):
    if platf == 'lin': #platform check
        if len(path.strip()) != 0: #did the user enter the path
            try:
                with open(path, 'a') as f:
                    json.dump(data, f, indent=5, ensure_ascii= False)
            except NameError as n:  #if the path is incorrect - write to the standard path
                with open(f'/home/{username}/Рабочий стол/CoinMarket.json', 'a') as f:
                    json.dump(data, f, indent=5, ensure_ascii= False)
                    print(n)
                    print('Saved to standard path (Desktop)')
        else:      #if the user has not entered the path, write to the standard path
            with open(f'/home/{username}/Рабочий стол/CoinMarket.json', 'a') as f:
                json.dump(data, f, indent=5, ensure_ascii=False)
    elif platf == 'win':
        if len(path.strip()) != 0:
            try:
                with open(path, 'a') as f:
                    json.dump(data, f, indent=5, ensure_ascii=False)
            except NameError as n:
                with open(f'C:\{username}\Рабочий стол\CoinMarket.json', 'a') as f:
                    json.dump(data, f, indent=5, ensure_ascii=False)
                    print(n)
                    print('Saved to standard path (Desktop)')
        else:       
            with open(f'/home/{username}/Рабочий стол/CoinMarket.json', 'a') as f:
                json.dump(data, f, indent=5, ensure_ascii=False)
    else: #if unknown platform
        with open(f'CoinMarket.json', 'a') as f:
            json.dump(data, f, indent=5, ensure_ascii=False)
    
    
if __name__ == '__main__':
    session = Session()#session creation
    session.headers.update(headers)
    while True:
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        if len(data):
            get_info(data)
        sleep(int(time_for_sleep))