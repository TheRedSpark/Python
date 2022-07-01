from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup  # V4.10.0
import time
from package import variables as v

active_scraper = False
save_to_txt = True
login_status = False
headless = False
base_url = 'https://selma.tu-dresden.de/APP/EXTERNALPAGES/-N000000000000001,-N000155,-AEXT_willkommen'


def logoff(login_status):
    if login_status:
        browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/div/form/div/input[1]").click()
        time.sleep(1)


if active_scraper:
    # Checking if the headless variable is true or false. If it is true, it will open a headless browser. If it is false,
    # it will open a normal browser.
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

    time.sleep(3)
    print("Baseurl getted")

    # Logging in to the selma website and then clicking on the "Prüfungsverwaltung" and then on "Ergebnisse"
    browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div/div[1]/input").send_keys(
        v.selma_benutzer)
    browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div/div[2]/input").send_keys(
        v.selma_pass)
    login_status = True

    time.sleep(0.5)

    browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input[9]").click()
    time.sleep(1)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li/ul/li[3]/a").click()
    time.sleep(1)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li/ul/li[3]/ul/li[2]/a").click()
    time.sleep(1)
    html = browser.page_source
    browser.quit()

# Saving the html code to a txt file.
if save_to_txt:
    text_file = open("data.txt", "w")
    text_file.write(html)
    text_file.close()

elif active_scraper:
    pass

else:
    text_file = open("data.txt", "r")
    html = text_file.read()
    text_file.close()

soup = BeautifulSoup(html, 'html.parser')
exam_all = soup.find_all('tr', attrs={'class': 'tbdata'})
anzahl_prufungen = len(exam_all)
i = 0
# A while loop that iterates through all the exams and prints the exam_kennung, exam_beschreibung, exam_date, exam_mark
# and exam_comment.
while True:
    exam_single = exam_all[i].find_all('td')
    del exam_single[4]
    # Removing the html tags from the string.
    exam_head = str(exam_single[0]).replace("<td>", "").replace("<br/>", " ").replace("</td>", "").replace(f'\t\t\t\t',
                                                                                                           '').replace(
        f'\n',
        '').replace(
        f'\xa0', 'uahsdiuahwekj').replace("  ", "").split("uahsdiuahwekj")
    del exam_head[1]
    # The first element of the list is the exam_kennung and the second is the exam_beschreibung.
    exam_kennung = exam_head[0]
    exam_beschreibung = exam_head[1]
    # Removing the html tags from the string.
    exam_date = str(exam_single[1]).strip().replace(f'<td style="vertical-align:top;">', '').replace("</td>",
                                                                                                     "").strip()
    exam_mark = str(exam_single[2]).strip().replace(f'<td style="vertical-align:top;">', '').replace("</td>",
                                                                                                     "").strip()
    exam_comment = str(exam_single[3]).strip().replace(f'<td style="vertical-align:top;">', '').replace("</td>",
                                                                                                        "").strip()

    print(exam_kennung)
    print(exam_beschreibung)
    print(exam_date)
    print(exam_mark)
    print(exam_comment)

    i = i + 1
    if i == anzahl_prufungen:
        break
logoff(login_status)
