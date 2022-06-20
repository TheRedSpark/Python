from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options

i = 0
from package import variables as v
options = Options()
options.headless = True
base_url = 'https://orteil.dashnet.org/cookieclicker/'
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(base_url)
time.sleep(5)
browser.find_element_by_xpath("/html/body/div[1]/div/a[1]").click()  # cookies
browser.find_element_by_id("langSelect-DE").click()  # sprache
time.sleep(10)
bigcookie = browser.find_element_by_id("bigCookie")
for a in range(100):
    bigcookie.click()
    time.sleep(0.01)


def clicking():
    for a in range(100):
        bigcookie.click()


# oma.click()

a = 2
while True:
    # cookies = int(str(browser.title.replace(" Kekse - Cookie Clicker", "")).replace(",",""))
    list = str(browser.find_element_by_xpath("/html/body/div/div[2]/div[15]/div[4]").text).replace(",", "").replace(" Kekse", "").replace(" Keks","").split("per")
    cookies = int(list[0])
    print(cookies)
    if i < 10 and int(str(browser.find_element_by_id(f'productPrice{a - 2}').text).replace(",", "")) < cookies:
        browser.find_element_by_xpath(f'/html/body/div/div[2]/div[19]/div[3]/div[6]/div[{a}]').click()
        time.sleep(0.3)
        i += 1
        continue
    elif i >= 10:
        a += 1
        i = 0
        print("")
    else:
        browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[5]/div").click()
    clicking()
print(cookies)
# browser.close()
