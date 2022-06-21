# Importing the webdriver, the chrome driver manager, the time module and the options module.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt # V3.5.2
import pandas as pd # V1.4.2

headless = False
base_url = 'https://orteil.dashnet.org/cookieclicker/'
anzahl_items = 0
gernerale_items = 2

if headless:
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options,
                               executable_path=r'C:\Users\Win10\.wdm\drivers\chromedriver\win32\102.0.5005.61'
                                               r'\chromedriver.exe')
    browser.get(base_url)
    print("Headless Chrome Initialized")

else:
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(base_url)

time.sleep(5)
print("Baseurl getted")
browser.find_element_by_xpath("/html/body/div[1]/div/a[1]").click()  # cookies
browser.find_element_by_id("langSelect-DE").click()  # sprache
time.sleep(10)
print("Mainpage Loaded")
bigcookie = browser.find_element_by_id("bigCookie")


def clicking(press):
    print("")
    print("Now Clicking " + str(press))
    for numbers in range(press):
        bigcookie.click()
        if numbers % 25 == 0:
            print(numbers)


clicking(50)

while True:
    list = str(browser.find_element_by_xpath("/html/body/div/div[2]/div[15]/div[4]").text).replace(",", "").replace(
        " Kekse", "").replace(" Keks", "").split("per")
    cookies = int(list[0])
    sec_clicks = (list[1].replace(" second:","") + " Cookies pro Sekunde")
    print(str(cookies) + " Cookies")
    print(sec_clicks)
    if anzahl_items < 10 and int(
            str(browser.find_element_by_id(f'productPrice{gernerale_items - 2}').text).replace(",", "")) < cookies:
        browser.find_element_by_xpath(f'/html/body/div/div[2]/div[19]/div[3]/div[6]/div[{gernerale_items}]').click()
        time.sleep(0.3)
        anzahl_items += 1
        continue
    elif anzahl_items >= 10:
        gernerale_items += 1
        anzahl_items = 0
        print("")
    else:
        time.sleep(1)
        if not headless:
            browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[5]/div").click()
            time.sleep(1)
        else:
            time.sleep(0.1)
    clicking(100)
# browser.close()
