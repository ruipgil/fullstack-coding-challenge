import os
from Story import Story
from pymongo import MongoClient

MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
client = MongoClient(
    'localhost' if MONGO_HOST is None else MONGO_HOST,
    27018 if MONGO_PORT is None else int(MONGO_PORT)
)
db = client.test

""" Database structure:
    stories: [{ id, title, author, ... }]
    top_stories: [{ top: [] }] #only one record
"""

def previous_top_stories():
    """ Gets a list of the previous top stories ids

    Returns:
        list of int
    """
    tops = db.top_stories.find_one()
    return tops['top'] if tops is not None else []

def save_top_stories(tops):
    """ Updates the list of top stories

    Args:
        tops (list of int)
    """
    if db.top_stories.count() == 0:
        db.top_stories.insert_one({'top': tops})
    else:
        db.top_stories.update_one({}, {'$set': {'top': tops}})

def find_story(story_id):
    """ Finds a story

    Args:
        story_id (int)
    Returns:
        :obj:`Story` or none
    """
    story = db.stories.find_one({'id': story_id})
    if story is None:
        return None
    else:
        return Story.from_db(story)

def save_story(story):
    """ Saves a story instance

    Args:
        story (:obj:`Story`)
    """
    if db.stories.find_one({'id': story.id}) is None:
        db.stories.insert_one(story.to_json())
