from bs4 import BeautifulSoup
import requests as rq
import re
import pandas as pd

# ombyg det til at indlæse den seneste titel i variablen latest og tjek den mod scraperen.
try:
    heste_df = pd.read_csv('test.csv')  # opens the heste dataframe so we can save our findings
except:
    pass

response = rq.get('https://www.heste-nettet.dk/forum/27/')  # TODO tilføj url

horse_soup = BeautifulSoup(response.text, 'html.parser')

url_prefix = "https://www.heste-nettet.dk"

latest = '[FLYTTET] Mødregruppe'

new_posts = {}

new_post_counter = 0   # TODO write this as a function so i can get the different forums! 
for post in horse_soup.find_all('tr', valign='middle'):  # could we remove this one, and search directly for td?
    for info in post.find_all('td'):
        try:
            url = info.find('a')['href']  # finds the url of the post
            title = info.find('a').text  # finds the title of the post
            category = post.find_all('td')[1].text  # finds the category
            author = post.find_all('td')[3].text  # finds the author
            replies = post.find_all('td')[4].text  # finds the amount of replies
            read = post.find_all('td')[5].text  # finds the amount of times the post has been read
            #print(url, title, category, author, replies, read)
        except TypeError:  # catches the errors when it finds something that is not a post.
            continue
    if title == latest:
        break
    else:
        new_posts[new_post_counter] = {'url': url, 'title': title, 'category': category, 'author': author,
        'replies': replies, 'read': read}
        new_post_counter += 1

print(new_posts)

post_df = pd.DataFrame.from_dict(new_posts, orient='index')
post_df.to_csv('test.csv')

def get_comments(dic):  # TODO write it as a function so it can get comments! 
    """takes a dic of dicts with a hestenet url, and fetches comments"""
    for post in dic:
        temp = rq.get(url_prefix + dic[post]['url'])
        post_soup = BeautifulSoup(temp.text, 'html.parser') 
        comments = []
        for reply in post_soup.find_all('div', class_='rsPost') # finder ikke alle kommentarer, men kun
        # hovedsvaret! Tror jeg. 

        


    
 


#for comment in horse_soup.find_all('div', class='rsPost'):
