from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1
import time

url = f'https://www.kaufland.de/product/384347866/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = float(str(soup.find('span', attrs={'class': 'rd-price-information__price'}).text.strip().replace(" €","")).replace(",","."))
#price = table.replace("<span class="rd-price-information__price">","").replace("</span>")
print("Kaufland")
print(table)



url = f'https://www.amazon.de/Sony-Interactive-Entertainment-PlayStation-5/dp/B08H93ZRK9/ref=sr_1_1?ascsubtag=CM1S1P1A1397593Z&keywords=playstation%2B5&linkCode=ll2&linkId=08027ea4b7cbc8d3a39c2f872c4b881f&qid=1655829778&sprefix=play%2Caps%2C150&sr=8-1'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = str(soup.find('span', attrs={'class' : 'a-price-whole'}).text)
print("Amazone")
print(table)