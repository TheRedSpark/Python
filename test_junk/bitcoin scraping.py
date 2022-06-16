from bs4 import BeautifulSoup # V4.10.0
import requests # V2.27.1
import time
import mysql.connector # V8.0.28
from package import zugang as anbin #Own Library
ort = 'lap'
#database = 'numbeo'
# mydb = mysql.connector.connect(
#         host=anbin.host(ort),
#         user=anbin.user(ort),
#         passwd=anbin.passwd(ort),
#         database="bitcoin",
#         auth_plugin='mysql_native_password')
#
# my_cursor = mydb.cursor()

url = f'https://www.coingecko.com/de'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table', attrs={'class': 'sort table mb-0 text-sm text-lg-normal table-scrollable'})
#rows = table.find_all('tr')
print(table)