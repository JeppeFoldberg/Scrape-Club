from bs4 import BeautifulSoup
import requests as rq
import re
import pandas as pd

heste_df = pd.read_csv('heste_info.csv')  # opens the heste dataframe so we can save our findings

response = rq.get('https://www.heste-nettet.dk/forum/27/')  # TODO tilføj url

horse_soup = BeautifulSoup(response.text, 'html.parser')

url_soeg = re.compile('/forum/27/')

#print(horse_soup.find_all('tr', valign='middle'), "\nnew search \n")

for post in horse_soup.find_all('tr', valign='middle'):
    for info in post.find_all('td'):
        try:
            url = info.find('a')['href']
            title = info.find('a').text
        except TypeError:
            continue
        #print(info.find('a').text)
    #print(info[1], info[2], info[3])
#print(horse_soup.find_all('a'))


#for comment in horse_soup.find_all('div', class='rsPost'):
