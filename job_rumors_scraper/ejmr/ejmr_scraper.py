import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re





def ejmr_page_urls(from_page, to_page, sub_forum = 'not_specified'):
    """
    ejmr_page_urls is used to gather the URL's for threads on econjobrumors.com. 
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
            url_list = [base_url] + [url + str(i + 1) for i in page_index] # base_url is page 1
            url_list.pop()# remove last element, otherwise to_page + 1
        else:
            url_list = [url + str(i) for i in page_index]
    
    else:
        sub_url = base_url + 'forum/' + sub_forum + '/page/' 
        url_list = [sub_url + str(i) for i in page_index]
    
    return url_list
   

def ejmr_content_urls(page_url_list):
    # loop over urls list of thread page responses
    responses_list = [requests.get(url) for url in page_url_list]

    # loop over responses to create a list of soup objects
    soup_list = [BeautifulSoup(response.text, 'html.parser') for response in responses_list]

    # list to store thread content url
    content_urls = []

    for page in soup_list:
        # find body content
        page = page.find('body')

        #loop over thread href
        for thread in page.find_all('tr'):

            # regex to extract urls only containing topic
            regex = '(?:https?|ftp)://[\w-]+(?:\.[\w-]+)+/(?:[\w.,@^=%&:/~+-]*/)?topic/(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
            # extract thread urls
            thread = re.findall(regex, str(thread))
            
            if thread:
                content_urls.append(thread[0])

    return content_urls



    # list of returned thread urls
    

        
        









