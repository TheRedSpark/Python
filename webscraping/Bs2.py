from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1

url = f'https://www.finanzen.net/devisen/bitcoin-euro-kurs'


def btc():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('div', attrs={'class': 'col-xs-5 col-sm-4 text-sm-right text-nowrap'})
    rows = table.find_all('div')

    price = float(
        str(rows).replace("</span></div>]", "").replace("<span>", "").replace("[<div>", "").replace("EUR", "").replace(
            ".", "").replace(",", "."))

    print(f'{price} Euro')
    return price
