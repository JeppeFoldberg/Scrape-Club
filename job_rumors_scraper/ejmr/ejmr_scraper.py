#!/usr/bin/env python

"""
This is a scraper for the economics forum Econ job market rumors.
"""

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

        # loop over soup list containing
        for page in soup_list:
            #loop over threads
            for thread in page.find_all('tr'):

                thread_url =  thread.find_all('a')
                thread_url = thread_url[0].get('href')

                if thread_url == 'http://www.econjobrumors.com/?new=1':
                    pass
                else:
                    thread_urls.append(thread_url)

                # get page count
                page_count = thread.find('td', {'class':'num'})
                if page_count:
                    page_count = math.ceil(int(page_count.text) / 20) # there are 20 posts per thread page
                    pages_count.append(page_count)


    # create dictionary with url and page_count as
    thread_url_dict = dict(zip(thread_urls, pages_count))



    return thread_url_dict


def all_page_urls():


    urls_dict = {}

    url = 'https://www.econjobrumors.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    header = soup.find('ul', {'class':'new-nav'})
    forums = header.find_all('a')

    for link in forums:
        if link.has_attr('href') and link.find('span', {'class':'headp'}) is not None:


            urls_dict[link['href']] = link.find('span', {'class':'headp'}).text




    return urls_dictef all_page_urls():



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
    Argument: Dict of thread urls extracted with thread_urls, if the ouput should be stored locally.
    Returns: List with soup object. Each element is one page. If stored locally - dumps pickle file.
    """
    # get full list of urls (one for each page in each thread)
    url_list = []
    responses_list = [] # store responses

    for url, count in thread_url_dict.items():
        base_url = url + '/page/' # correct url format
        url_list.append([base_url + str(i + 1) for i in range(count)])

    # get html for each page och each thread
    # loop over threads
    for thread in tqdm(url_list):
        try:
            # loop over urls in thread
            response = [requests.get(url) for url in thread]
            responses_list.append(response)

        except:

            continue

    if store_locally == 1:
        # file name format
        file_name = 'ejhr_' + str(len(thread_url_dict)) + '_threads_' + str(datetime.date.today())

        with open(file_name, 'wb') as fp:
                pickle.dump(responses_list, fp)

    return responses_list



def page_df(page_responses_list, store_locally = 0): #1 for yes
    """
    Creates Pandas df of ejmr page content.
    Argument: list of html objects parsed with dump page content, 1 if the ouput should be stored locally.
    Returns: Pandas DataFrame and if asked a csv locally.
    """

    # create list of soup objects

    soup_list = [BeautifulSoup(url.text, 'html.parser') for url in page_responses_list]

    title_list = [] # the title of the thread
    post_count_list = [] # amount of posts in thread
    views_list = [] # how many times the post has been viewed
    latest_post_list = []
    positive_votes_list = []
    negative_votes_list = []
    vote_ratio_list = []
    thread_url_list = []

    # loop over pages
    for page in tqdm(soup_list):
        # find body content
        page = page.find('table', {'id':'latest'})
        #loop over threads
        for thread in page.find_all('tr'):

            # find thread title
            title = thread.find('a', href = True)

            # continue if it cathces new topic
            if 'New Topic »' in title.text:
                continue
            else:

                # get title
                title = title.text
                title_list.append(title)

                # get post counts, views and votes
                count_views_votes = thread.find_all('td', {'class':'num'})
                if count_views_votes:
                    #amount of posts
                    post_count = count_views_votes[0].text
                    post_count_list.append(int(post_count))
                    #views
                    views = count_views_votes[1].text
                    views_list.append(int(views))

                    #latest post / freshness
                    latest_post = count_views_votes[3].text
                    latest_post_list.append(latest_post)

                    #postive/negative votes
                    votes = count_views_votes[2].text

                    # transform votes to something more interesting
                    votes = votes.split('-')
                    positive_votes = int(votes[0])
                    negative_votes = int(votes[1])

                    # check if denominator > 0
                    if (positive_votes + negative_votes) > 0:
                        vote_ratio = positive_votes / (positive_votes + negative_votes)
                    else:
                        vote_ratio = np.NaN

                    # get thread url
                    thread_url =  thread.find_all('a')
                    thread_url = thread_url[0].get('href')

                    if thread_url == 'http://www.econjobrumors.com/?new=1':
                        pass
                    else:
                        thread_url_list.append(thread_url)

                    positive_votes_list.append(positive_votes) # amount of positive votes
                    negative_votes_list.append(negative_votes) # amount of negative votes
                    vote_ratio_list.append(vote_ratio) # ratio of positive votes


    # create pandas df
    page_df = pd.DataFrame(list(zip(title_list, post_count_list, views_list,
                                     positive_votes_list, negative_votes_list,
                                     vote_ratio_list, latest_post_list, thread_url_list)),
                                     columns =['title', 'posts', 'views',
                                               'positive_votes', 'negative_votes',
                                               'vote_ratio', 'latest_post', 'thread_url'])



    if store_locally == 1:
        # file name format
        file_name = 'ejhr_posts_df' + str(datetime.date.today())
        # store csv locally
        page_df.to_csv(file_name)


    return page_df


def thread_df(thread_responses_list, store_locally = 0):
    """
    Creates Pandas df with thread content.
    Argument: list of thread html objects retrieved with dump_thread_content.
    Returns: List with soup object. Each element is one page. If stored locally - dumps pickle file.
    """


    soup_list = []
    for thread in tqdm(thread_responses_list):

        soup = [BeautifulSoup(page.text, 'html.parser') for page in thread]
        soup_list.append(soup)

    post_author = [] # 4 random characters if anonymous else user name
    post_author_rep = [] # NaN if anonymous else the reputation of author
    post_text = [] # full text
    post_likes = [] # good
    post_dislikes = [] # not good
    post_position = [] # the position in the thread
    post_age = []
    thread_name = [] # the name of the thread


    # loop over each thread
    for thread in tqdm(soup_list):

        # loop over each page in a thread
        for page in thread:


            # get author and reputation if not anonymous
            authors = page.find_all('div', {'class':'threadauthor'})

            # loop over authors
            for author in authors:
               # check if author is anonymous
                if author.text.split('\n')[2] == 'Economist':
                    post_author.append(author.text.split('\n')[3])
                    post_author_rep.append(np.NaN)
                # if registered user append user name and their reputation
                else:
                    post_author.append(author.text.split('\n')[2])
                    post_author_rep.append(author.text.split('\n')[3])

            # get text
            posts = page.find_all('div', {'class':'post'})
            [post_text.append(post.text) for post in posts]

            #TODO Implement functionallity for dealing with when posts quote and references other posts

            # get likes, dislikes and how old the post is
            likes_dislikes_age = page.find_all('div', {'class':'poststuff'})


            # likes
            [post_likes.append(int(re.findall('(?<=\>)(.*?)(?=\<)', str(like))[5])) for like in likes_dislikes_age]

            # dislikes
            [post_dislikes.append(int(re.findall('(?<=\>)(.*?)(?=\<)', str(dislike))[9])) for dislike in likes_dislikes_age]

            # post age
            [post_age.append(re.findall('(?<=\>)(.*?)(?=\<)', str(date))[0]) for date in likes_dislikes_age]


            # get position
            [post_position.append(position + 1) for position in range(len(posts))]

            # get title
            titles = page.find('h2', {'class':'topictitle'})
            for i in range(len(authors)):
                thread_name.append(titles.text)




    # create df
    thread_df = pd.DataFrame(list(zip(post_author, post_author_rep,
                                      thread_name, post_text,
                                      post_likes, post_dislikes,
                                      post_age, post_position)),
                                      columns =['author', 'author_rep',
                                                'tread_name', 'post_text',
                                                'post_likes', 'post_dislikes',
                                                'post_age', 'position'])


    return thread_df













