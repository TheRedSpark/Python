import requests

x = requests.get('https://netzfrequenzmessung.de:9081/frequenz02a.xml?c=916856')
print(x.text)
