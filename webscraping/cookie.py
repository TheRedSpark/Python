from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from package import variables as v
base_url = 'https://orteil.dashnet.org/cookieclicker/'
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(base_url)
time.sleep(5)
browser.find_element_by_xpath("/html/body/div[1]/div/a[1]").click()#cookies
browser.find_element_by_id("langSelect-DE").click()#sprache
time.sleep(10)
bigcookie = browser.find_element_by_id("bigCookie")
cursor = browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[6]/div[2]")
oma = browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[6]/div[3]")
farm = browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[6]/div[4]")
for a in range(1000):
    bigcookie.click()
    time.sleep(0.01)
#oma.click()
cookies = int(browser.title.replace(" Kekse - Cookie Clicker", ""))
while True:
    cursor.click()
    oma.click()
    farm.click()
    time.sleep(3)
print(cookies)
#browser.close()