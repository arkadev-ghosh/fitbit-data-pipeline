import requests
from bs4 import BeautifulSoup

url = 'http://125.19.52.218/realtime/'
html = requests.get(url=url)

s = BeautifulSoup(html.content,
                  'html.parser')

for tr in s.find_all('tr'):
    tds = tr.find_all('td')
    print(tds)

