import requests
from shinarnews.Story import Story

STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/%d.json'

def get_json(url):
    """ Sends a GET request to an url and decodes its body as json

    Args:
        url (str)
    Returns:
        dict
    """
    request = requests.get(url=url)
    return request.json()

def top_stories(top_n=10):
    """ Queries the Firebase API for the top_n stories

    Args:
        top_n (int): top stories to retrieve
    Returns:
        list of int: stories ids
    """
    # firebase's API allows a maximum of 500 top stories
    top_n = min(top_n, 500)

    stories = get_json(STORIES_URL)
    return stories[:top_n]

def get_item_details(story_id):
    """ Queries the Firebas API for the details of a story

    Args:
        story_id (int): story id to query
    Returns:
        :obj:`Story`
    """

    url = ITEM_URL % story_id
    item = get_json(url)

    return Story.from_json(item)
