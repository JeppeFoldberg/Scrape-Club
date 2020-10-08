import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
import pickle
import datetime
import math




def page_urls(from_page, to_page, sub_forum = 'not_specified'):
    """
    ejmr_page_urls is used to gather the URL's for pages of threads on econjobrumors.com. 
    Arguments: From page (Page number to start gathering from), to page and optionally a sub-forum name.
    Returns: A list of URL's.
    """ 
    
    # base ejmr url
    base_url = 'https://www.econjobrumors.com/'

    # create a page_index
    page_index = [(from_page + i) for i in range(to_page-from_page + 1)]
    

    # adapt url based on if sub-forum or not
    if 'not_specified' in sub_forum:
        #define url when no sub-forum
        url = base_url + 'page/'

        #the first page if not subforum has different formating
        if from_page <= 1:
            page_urls = [base_url] + [url + str(i + 1) for i in page_index] # base_url is page 1
            page_urls.pop()# remove last element, otherwise to_page + 1
        else:
            page_urls = [url + str(i) for i in page_index]
    
    else:
        sub_url = base_url + 'forum/' + sub_forum + '/page/' 
        page_urls = [sub_url + str(i) for i in page_index]
    
    return page_urls
   

def thread_urls(page_url_list):
    """
    ejmr_thread_urls is used to gather the URL's threads on econjobrumors.com. 
    Argument: Indivudual page url or list of page urls extracted with ejmr_page_urls.
    Returns: A dictionary of thread URL's as key and the page count as value.
    """ 
    # if just one url, turn to list
    if not isinstance(page_url_list, list):
        page_url_list = [page_url_list]

    # loop over urls list of thread page responses
    responses_list = [requests.get(url) for url in tqdm(page_url_list)]

    # loop over responses to create a list of soup objects
    soup_list = [BeautifulSoup(response.text, 'html.parser') for response in responses_list]

    # list to store thread content url
    thread_urls = []
    pages_count = []

    for page in soup_list:
        # find body content
        page = page.find('body')

        #loop over threads
        for thread in page.find_all('tr'):

            # regex to extract urls only containing topic
            regex = '(?:https?|ftp)://[\w-]+(?:\.[\w-]+)+/(?:[\w.,@^=%&:/~+-]*/)?topic/(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
            thread_url = re.findall(regex, str(thread)) # extract thread urls
            if thread_url:
                thread_urls.append(thread_url[0]) # extract first elemt. Second element is next page in same thread

            # get page count
            page_count = thread.find('td', {'class':'num'})
            if page_count:
                page_count = math.ceil(int(page_count.text) / 20) # there are 20 posts per thread page
                pages_count.append(page_count) 

    # create dictionary with url and page_count as
    thread_url_dict = dict(zip(thread_urls, pages_count))



    return thread_url_dict

def dump_page_content(page_url_list, store_locally = 0): #1 for yes
    """
    Retrieves and if asked dumps full page content from ejmr page.
    Argument: Indivudual page url or list of page urls extracted with ejmr_page_urls, if the ouput should be stored locally.
    Returns: List with soup object. Each element is one page. If stored locally - dumps pickle file.
    """
    # check if list or single url
    if not isinstance(page_url_list, list):
        page_url_list = [page_url_list]
    
    # loop over urls list of thread page responses
    responses_list = [requests.get(url) for url in tqdm(page_url_list)]

    # loop over responses and retrieve soup object
    #soup_list = [BeautifulSoup(response.text, 'html.parser') for response in responses_list]

    # dump if stored locally
    if store_locally == 1: 
        #file name format    
        file_name = 'ejhr_' + str(len(page_url_list)) + '_pages_' + str(datetime.date.today())
        
        with open(file_name, 'wb') as fp: 
                pickle.dump(responses_list, fp)

    return responses_list 

def dump_thread_content(thread_url_dict, store_locally = 0): #1 for yes
    """
    Retrieves and if asked dumps thread content from ejmr thread.
    Argument: Indivudual thread url or list of thread urls extracted with ejmr_thread_urls, if the ouput should be stored locally.
    Returns: List with soup object. Each element is one page. If stored locally - dumps pickle file.
    """
    
    soup_list = [BeautifulSoup(thread_url.text, 'html.parser') for thread in tqdm(thread_url_list)]


    
    thread_list = []



def page_df(page_responses_list):
    """
    Retrieves and if asked dumps full page content (thread_title, posts, views, votes etc) from ejmr page.
    Argument: Indivudual page url or list of page urls extracted with ejmr_page_urls, if the ouput should be stored locally.
    Returns: List with soup object. Each element is one page. If stored locally - dumps pickle file.
    """
    pass


def thread_df(thread_responses_list):
    """
    Retrieves and if asked dumps full page content (thread_title, posts, views, votes etc) from ejmr page.
    Argument: Indivudual page url or list of page urls extracted with ejmr_page_urls, if the ouput should be stored locally.
    Returns: List with soup object. Each element is one page. If stored locally - dumps pickle file.
    """
    pass






    # list of returned thread urls
    

        
        








