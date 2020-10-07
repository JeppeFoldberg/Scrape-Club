from bs4 import BeautifulSoup
import requests as rq
import re
#import pandas as pd

response = rq.get('https://www.heste-nettet.dk/forum/27/')  # TODO tilføj url

horse_soup = BeautifulSoup(response.text, 'html.parser')

url_soeg = re.compile('/forum/27/')

print(horse_soup.find_all('a'))


#for comment in horse_soup.find_all('div', class='rsPost'):
