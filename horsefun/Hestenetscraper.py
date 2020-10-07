from bs4 import BeautifulSoup
import requests as rq
import re
import pandas as pd

# ombyg det til at indlæse den seneste titel i variablen latest og tjek den mod scraperen.
heste_df = pd.read_csv('heste_info.csv')  # opens the heste dataframe so we can save our findings

response = rq.get('https://www.heste-nettet.dk/forum/27/')  # TODO tilføj url

horse_soup = BeautifulSoup(response.text, 'html.parser')

url_prefix = "https://www.heste-nettet.dk"

latest = '[FLYTTET] Mødregruppe'



for post in horse_soup.find_all('tr', valign='middle'):
    #print(post.find_all('td')[2].text)
    for info in post.find_all('td'):
        try:
            url = info.find('a')['href']  # finds the url of the post
            title = info.find('a').text  # finds the title of the post
            print(url, title)
        except TypeError:  # catches the errors when it finds something that is not a post.
            continue
    if title == latest:
        break
 


#for comment in horse_soup.find_all('div', class='rsPost'):
