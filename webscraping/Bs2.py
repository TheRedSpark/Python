from bs4 import BeautifulSoup # V4.10.0
import requests # V2.27.1
import time

url = f'https://www.finanzen.net/devisen/bitcoin-euro-kurs'
while True:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('div', attrs={'class': 'col-xs-5 col-sm-4 text-sm-right text-nowrap'})
    rows = table.find_all('div')

    #print(soup)
    #print(table)
    price = float(str(rows).replace("</span></div>]","").replace("<span>","").replace("[<div>","").replace("EUR","").replace(".","").replace(",","."))

    print(f'{price} Euro')
    time.sleep(1)