from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time



headless = False
base_url = 'https://selma.tu-dresden.de/APP/EXTERNALPAGES/-N000000000000001,-N000155,-AEXT_willkommen'

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