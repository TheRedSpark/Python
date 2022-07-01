from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1
import time
from package import variables as v

login_status = False
headless = False
base_url = 'https://selma.tu-dresden.de/APP/EXTERNALPAGES/-N000000000000001,-N000155,-AEXT_willkommen'
#
#
# if headless:
#     options = Options()
#     options.headless = True
#     browser = webdriver.Chrome(options=options,
#                                executable_path=r'C:\Users\Win10\.wdm\drivers\chromedriver\win32\102.0.5005.61'
#                                                r'\chromedriver.exe')
#     browser.get(base_url)
#     print("Headless Chrome Initialized")
#
# else:
#     browser = webdriver.Chrome(ChromeDriverManager().install())
#     browser.get(base_url)
#
# time.sleep(3)
# print("Baseurl getted")
#
#
# def logoff(login_status):
#     if login_status:
#         browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/div/form/div/input[1]").click()
#         time.sleep(1)
#
#
# browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div/div[1]/input").send_keys(
#     v.selma_benutzer)
# browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div/div[2]/input").send_keys(
#     v.selma_pass)
# login_status = True
#
# time.sleep(0.5)
#
# browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input[9]").click()
# time.sleep(1)
# browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li/ul/li[3]/a").click()
# time.sleep(1)
# browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li/ul/li[3]/ul/li[2]/a").click()
# time.sleep(1)
# html = browser.page_source
# browser.quit()
# text_file = open("data.txt", "w")
# text_file.write(html)
# text_file.close()




text_file = open("data.txt", "r")
html = text_file.read()
text_file.close()
soup = BeautifulSoup(html, 'html.parser')
# table = soup.find_all('tr', attrs={'style':'tbdata'})
#table = soup.find('table', attrs={'class': 'nb list'})
#prufungen = len(table)
#print(prufungen)

tablesub = soup.find_all('tr', attrs={'class': 'tbdata'})
prufungen = len(tablesub)
#rows = tablesub[2].find_all('td', attrs={'style': 'vertical-align:top;'})
rows = tablesub[1].find_all('td')
del rows[4]
kennung = str(rows[0]).strip().replace("<td>","").replace("<br/>"," ").replace("<br/></td>","").replace("</td>","").strip().replace(f' ','').replace(f'\t\t\t\t','').replace(f'\n','').replace("   ","").strip()#.split(" ")
date = str(rows[1]).strip().replace(f'<td style="vertical-align:top;">','').replace("</td>","").strip()
mark = str(rows[2]).strip().replace(f'<td style="vertical-align:top;">','').replace("</td>","").strip()
comment = str(rows[3]).strip().replace(f'<td style="vertical-align:top;">','').replace("</td>","").strip()

print(kennung)
print(date)
print(mark)
print(comment)

#print(rows)
#print(prufungen)
# print(soup)

# logoff(login_status)
