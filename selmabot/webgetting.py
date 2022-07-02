from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup  # V4.10.0
import time
from package import variables as v
import mysql.connector  # V8.0.28

active_scraper = True
save_to_txt = True
login_status = False
headless = True
base_url = 'https://selma.tu-dresden.de/APP/EXTERNALPAGES/-N000000000000001,-N000155,-AEXT_willkommen'
user_id = v.telegram_user_id
ort = 'home'
database = 'Selma'
exam_data_multi = [False]




def exam_getter(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')
    # Getting the username and password from the database.
    global exam_data_multi
    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Username_Selma,Password_Selma FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    result = my_cursor.fetchone()
    print(result)
    selma_benutzer = result[0]
    selma_pass = result[1]
    my_cursor.close()
    if selma_benutzer is not None and selma_pass is not None:
        pass
    else:
        return exam_data_multi

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
        print("Baseurl getted")
        while True:
            try:
                # Checking if the login form is loaded.
                browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form")
                print("Baseurl getted")
                break
            except:
                pass
                print("Website nicht bereit")

        # Logging in to the selma website and then clicking on the "Prüfungsverwaltung" and then on "Ergebnisse"
        browser.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div/div[1]/input").send_keys(
            selma_benutzer)
        browser.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div/div[2]/input").send_keys(
            selma_pass)

        while True:
            try:
                # Clicking on the login button.
                browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input[9]").click()
                print("Login Erfolgreich")
                login_status = True
                break
            except:
                pass
            print("Wait for Login")

        while True:
            try:
                # Clicking on the "Prüfungsverwaltung" button.
                browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li/ul/li[3]/a").click()
                print("Login-Website nicht bereit")
                login_status = True
                break
            except:
                pass
            print("Wait for Login-Website")

        while True:
            try:
                # Clicking on the "Prüfungsverwaltung" button.
                browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/ul/li/ul/li[3]/ul/li[2]/a").click()
                print("Prüfungsergebnisse-Website bereit")
                login_status = True
                break
            except:
                pass
            print("Prüfungsergebnisse-Website bereit")

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
        exam_head = str(exam_single[0]).replace("<td>", "").replace("<br/>", " ").replace("</td>", "").replace(
            f'\t\t\t\t',
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
        if exam_date == "":
            exam_date = "Kein Datum vorhanden"

        exam_mark = str(exam_single[2]).strip().replace(f'<td style="vertical-align:top;">', '').replace("</td>",
                                                                                                         "").strip()
        exam_comment = str(exam_single[3]).strip().replace(f'<td style="vertical-align:top;">', '').replace("</td>",
                                                                                                            "").strip()

        # print(exam_kennung)
        # print(exam_beschreibung)
        # print(exam_date)
        # print(exam_mark)
        # print(exam_comment)
        # print()
        exam_data_single = [exam_kennung, exam_beschreibung, exam_date, exam_mark, exam_comment]
        exam_data_multi = exam_data_multi + exam_data_single
        i = i + 1
        if i == anzahl_prufungen:
            break

    exam_data_multi = exam_data_multi + [str(anzahl_prufungen)]
    return exam_data_multi
#     logoff(login_status)
#
#
# def logoff(login_status):
#     if login_status:
#         browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[2]/div/form/div/input[1]").click()
#         time.sleep(1)
# exam_getter(v.telegram_user_id)
