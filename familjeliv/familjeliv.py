import requests
import pandas as pd
import pickle
from bs4 import BeautifulSoup
import datetime
import time
import re
from tqdm import tqdm
import numpy as np



def get_threads(from_page, to_page):
    """
    Argument: Range of familjeliv pages to be scraped
    Returns: Pandas DataFrame stored as csv containing information of the threads
    """
    # define base url
    base_url = 'https://www.familjeliv.se/forum/new/'

    # list of page idexes to iterate over
    page_index = [(from_page + i) for i in range(to_page-from_page + 1)]
    
    # create list of urls to loop over
    url_list = [base_url + str(i) for i in page_index]

    # loop over urls list of thread page responses
    responses_list = [requests.get(response) for response in url_list]
    
    # loop over responses for list of soup objects
    soup_list = [BeautifulSoup(response.text, 'html.parser') for response in responses_list]

    
    title_list = [] # containing thread title
    thread_url_list = [] # the unique thread url
    category_list = [] # thread category
    replies_list = [] # reply count on thread
    created_by_list = [] # the user who started the thread
    date_list = [] # the date the thread was created
    time_list = [] # the time the thread was created

    # get page information
    for page in soup_list:
        # get thread
        for thread in page.find_all('tr', {'class': ''}):
            
            # get title and thread url
            title_url = thread.find('a')
            title_url = re.findall('"(.*?)"', str(title_url)) # get string element between quotes
            # the first element "a" is always empty
            if title_url:
                title_list.append(title_url[1])
                thread_url_list.append(title_url[0])

            # get category
            category = thread.find('td', {'class':'forum'})
            # the first element "td" is always empty
            if category:
                category = re.findall('(?<=\>)(.*?)(?=\<)', str(category))[0] # get string between > <
                category = str(category).replace('&amp', '&').replace('&;', '&') # manually replace some uggliness
                category_list.append(category)

            # get created by user 
            user = thread.find('span', {'class':'nick'})
            if user:
                #print(user)
                user = re.findall('(?<=\>)(.*?)(?=\<)', str(user)) # get strings between > <
                # if user is anonymous list == 1
                if len(user) == 1:
                    created_by_list.append(user[0])
                # if the user is not
                else:
                    #user = re.findall('>[\s\S]*$', str(user))[0]
                    user = str(user).split('>')[1].replace('\\xad', '') 
                    user = user.split("'")[0]
                    created_by_list.append(user)
                    #print(user)
                
            # get time/date created
            time_date = thread.find('td',{'class':'threadStarted'})
            if time_date:
                # extract time from string
                try:
                    time = re.findall('\d{1,2}:\d{2}', str(time_date))[0]
                    time_list.append(time)
                except:
                    time_list.append(np.NaN)

                
                # extract date from string
                if 'Idag' in str(time_date):
                    date = datetime.date.today()
                elif 'Igår' in str(time_date):
                    today = datetime.date.today()
                    date = today - datetime.timedelta(days=1)
                elif 'I förrgår' in str(time_date):
                    today = datetime.date.today()
                    date = today - datetime.timedelta(days=2)
                else:
                    date = re.findall('\d{4}-\d{2}-\d{2}', str(time_date))[0]

                date_list.append(date)
            
            # get replies
            reply = thread.find('td', {'class':'replies'})
            if reply:
                reply = re.findall('[\d]+', str(reply))[0]
                replies_list.append(int(reply))
                


    
    thread_df = pd.DataFrame(list(zip(title_list, category_list, replies_list, 
                                        created_by_list, date_list, time_list, 
                                        thread_url_list)), 
                                         columns =['title', 'category', 
                                        'replies_count', 'created_by', 
                                        'date_posted', 'time_created', 
                                        'url'])
                                
    # create csv title
    title = 'familjeliv_thread_dump_' + str(datetime.date.today())
    
    thread_df.to_csv(title)


    return thread_df


def get_urls(from_page, to_page):
    """
    Argument: Range of familjeliv pages 
    Returns: Returns list of the thread urls 
    """
    # define base url
    base_url = 'https://www.familjeliv.se/forum/new/'

    # list of page idexes to iterate over
    page_index = [(from_page + i) for i in range(to_page-from_page + 1)]
    
    # create list of urls to loop over
    url_list = [base_url + str(i) for i in page_index]

    # loop over urls list of thread page responses
    responses_list = [requests.get(response) for response in url_list]
    
    # loop over responses for list of soup objects
    soup_list = [BeautifulSoup(response.text, 'html.parser') for response in responses_list]

    # initiate empty list to store individual thread urls
    thread_url_list = [] # the unique thread url

    # get page information
    for page in soup_list:
        # get thread
        for thread in page.find_all('tr', {'class': ''}):
            
            # get title and thread url
            url = thread.find('a')
            url = re.findall('"(.*?)"', str(url)) # get string element between quotes
            # the first element "a" is always empty
            if url:
                base_thread_url = 'https://www.familjeliv.se'
                thread_url_list.append(base_thread_url + url[0])

    file_name = 'thread_urls_' + str(datetime.date.today())
    
    with open(file_name, 'wb') as fp: 
            pickle.dump(url_list, fp)
    
    return thread_url_list