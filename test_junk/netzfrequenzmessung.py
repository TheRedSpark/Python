import requests
import math as Math
import random
import  time


def generate_url():
    client = round(random.randint(0, 10000) * 10) * 31
    print(client)
    url = f'https://netzfrequenzmessung.de:9081/frequenz02a.xml?c={client}'
    return url


##Math.round(Math.random()*100000)*31
while True:
    x = requests.get(generate_url())
    y = x.text.splitlines()
    # print(y)
    netzfrequenz = y[1].replace("<f2>", "").replace("</f2>", "")
    zeit = y[3].replace("<z> ", "").replace("</z>", "")

    print(zeit)
    print(netzfrequenz)
    time.sleep(1)

