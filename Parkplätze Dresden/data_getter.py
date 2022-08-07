from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1
import time
import mysql.connector  # V8.0.28
from package import zugang as anbin

url = "https://www.dresden.de/apps_ext/ParkplatzApp/index"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('div', attrs={'class': 'element element_table responsiveTable'})

#print(len(table))
i = 0
a = 0
for orte in table:
    rows = table[i].find_all('tr')
    i = i + 1
    for platze in rows:
        simple_rows = rows[a].text.split("\n")
        innere_altstadt = [feld for feld in simple_rows if feld != '']
        if a == 0:
            print(innere_altstadt[0])
        else:
            print(innere_altstadt)
            # print(a)
        a = a + 1
    a = 0
