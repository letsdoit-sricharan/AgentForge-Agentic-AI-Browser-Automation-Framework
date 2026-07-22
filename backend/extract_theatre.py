import bs4
import re

with open('bms_test_failure.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

time_node = soup.find(string=re.compile('10:10 PM'))
if time_node:
    curr = time_node.parent
    for _ in range(15):
        if not curr: break
        if 'Cinepolis' in curr.text:
            print(f"FOUND common ancestor: {curr.name} with classes: {curr.get('class')}")
        curr = curr.parent
