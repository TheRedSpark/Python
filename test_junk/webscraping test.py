"""""""""
Kleines Skript welches automatisch die Einzelwerte von der Seite Numbeo abruft und diese anschließend automatisch 
in einen SQL Server speichert.Dies ist nur ein kleiner Test um mit der Libary Bs4 vertraut zu werden.
"""
from bs4 import BeautifulSoup # V4.10.0
import requests # V2.27.1


city_1 = 'Hanover'

url = f'https://www.numbeo.com/cost-of-living/in/{city_1}'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table',attrs={'class':'data_wide_table new_bar_table'})
rows = table.find_all('tr')
#test= "fun ist ?"
data = rows[3].text.split()
milk_price_raw = data[3].replace(",","")
price_range = data[5].replace(",","")
price_3 = price_range.split("-")
#milk_price_min = float(price_3[0])
#milk_price_max = float(price_3
#find(rows
print(data)
fail = data.pop()
data = data.append("fail")
#print(fail)
print(data)
#print(milk_price_raw)
#print(type(data))
#test = data.pop()
#test2= test.find()
#print(test)
#if data.pop().rfind('?') == 0:
#    print("keine Datenvorhanden")
#else:
#    pass

#print("weiter")
#print(test2)
#print(data[4])
#print(milk_price_raw)
print(price_range)