# Job Rumor Scraper

This is a container for scrapers of the following forums:

1. https://www.econjobrumors.com/
2. https://www.poliscirumors.com/
3. https://www.socjobrumors.com/

## Goals

The goal is for the scapers is to be able to produce two different data-frames, one in which each observation is a thread the forum (we call this page_df) and one where each observation is a post in a thread (we call this thread_df).

**page_df features**

  * Thread title
  * Thread subforum
  * Post count
  * Views
  * Positive votes
  * Negative votes
  * Freshness (the time of the last post in the thread - reverse chronological order)
  * Dowloaded timestamp 
  
**thread_df features**

  * Author
  * Author reputation
  * Post text
  * Post likes
  * Post dislikes
  * Post position in thread
  * Post time
  * Thread title
  * Downloaded timestamp
  * If post quotes other post, then for each quote:
    * Quote text
    * Quote text position
