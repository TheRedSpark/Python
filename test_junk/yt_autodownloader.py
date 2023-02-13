from pytube import YouTube
from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1

url = 'https://www.youtube.com/@Simplicissimus/videos'
def downloader(link: str):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    youtubeObject.download('videos')


page = requests.get(url, cookies={'CONSENT': 'PENDING+839'})
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
table = soup.find_all('div', attrs={'id': 'content'})
print(table)
table = soup.find_all("class = style-scope ytd-browse grid grid-5-columns")
print(table)
