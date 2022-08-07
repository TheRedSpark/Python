from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1
import time
import mysql.connector  # V8.0.28
from package import zugang as anbin


url = "https://www.dresden.de/apps_ext/ParkplatzApp/index"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)
table = soup.find('div', attrs={'column size8'})
option = table.find_all("Innere Altstadt")
#print(option)
print(table)
#rows = table.find_all('tr')