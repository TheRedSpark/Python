from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from package import variables as v
base_url = 'https://www.instagram.com/'
user = 'gartenkartoffel'
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(base_url)
time.sleep(5)
browser.find_element_by_xpath("/html/body/div[4]/div/div/button[1]").click()
time.sleep(2)
browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input").send_keys(v.usernameinsta)
browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input").send_keys(v.passwordinsta)
time.sleep(2)
browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button").click()
time.sleep(8)
browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
time.sleep(3)
browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
time.sleep(5)
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]").click()
time.sleep(3)
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys("gartenkartoffel")
time.sleep(3)
browser.get(base_url + user)
browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()