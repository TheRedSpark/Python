# Importing the webdriver, the chrome driver manager, the time module and the options module.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options

headless = True
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
browser.find_element_by_xpath("/html/body/div[1]/div/a[1]").click()  # cookies
browser.find_element_by_id("langSelect-DE").click()  # sprache
time.sleep(10)
bigcookie = browser.find_element_by_id("bigCookie")


def clicking(press):
    for numbers in range(press):
        bigcookie.click()


clicking(200)

while True:
    list = str(browser.find_element_by_xpath("/html/body/div/div[2]/div[15]/div[4]").text).replace(",", "").replace(
        " Kekse", "").replace(" Keks", "").split("per")
    cookies = int(list[0])
    print(cookies)
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
        browser.find_element_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[5]/div").click()
    clicking(100)
# browser.close()
