from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
i = 0
from package import variables as v
base_url = 'https://orteil.dashnet.org/cookieclicker/'
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(base_url)
time.sleep(5)
browser.find_element_by_xpath("/html/body/div[1]/div/a[1]").click()#cookies
browser.find_element_by_id("langSelect-DE").click()#sprache
time.sleep(10)
bigcookie = browser.find_element_by_id("bigCookie")
for a in range(1000):
    bigcookie.click()
    time.sleep(0.01)
#oma.click()

a = 2

while True:
    cookies = int(str(browser.title.replace(" Kekse - Cookie Clicker", "")).replace(",",""))
    print(cookies)
    if i < 10 and int(str(browser.find_element_by_id(f'productPrice{a-2}').text).replace(",","")) < cookies:
        browser.find_element_by_xpath(f'/html/body/div/div[2]/div[19]/div[3]/div[6]/div[{a}]').click()
        i += 1
    elif i >= 10:
        a += 1
        i = 0
        print("")
    else:
        browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[5]/div").click()
    time.sleep(0.5)
print(cookies)
#browser.close()
