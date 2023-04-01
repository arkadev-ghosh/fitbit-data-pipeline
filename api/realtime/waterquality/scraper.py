import re

import requests
from bs4 import BeautifulSoup

url = 'http://125.19.52.218/realtime/'
html = requests.get(url=url)

s = BeautifulSoup(html.content,
                  'html.parser')

pattern = re.compile(r'[A-Za-z0-9]{4}-.*', re.IGNORECASE)
mapping = {}

current_source = None
for tr in s.find_all('tr'):
    tds = tr.find_all('td')

    for elem in tds:
        elem_text = elem.text
        if pattern.match(elem_text):
            mapping[elem_text] = []
            current_source = elem_text

        else:
            mapping[current_source].append(elem_text)


for k,v in mapping.items():
    print(k)
    print(v)





