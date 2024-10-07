import requests
from bs4 import BeautifulSoup


# url = 'https://medlineplus.gov/ency/encyclopedia_A.htm'
# url = 'https://medlineplus.gov/ency/article/003123.htm'
url = 'https://medlineplus.gov/ency/article/001592.htm'

# request the url and save the html code and save it in sample.html file
r = requests.get(url)
with open('disease.html', 'w') as f:
    f.write(r.text) 
