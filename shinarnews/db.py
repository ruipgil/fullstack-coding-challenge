import os
from Story import Story
from pymongo import MongoClient

MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
client = MongoClient(
    'localhost' if MONGO_HOST is None else MONGO_HOST,
    27017 if MONGO_PORT is None else int(MONGO_PORT)
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

def update_story(story):
    """ Updates a story

    Args:
        story (:obj:`Story`)
    """
    db.stories.update_one({'id': story.id}, {'$set': story.to_json()})

def has_translation_waiting(story_id):
    """ Checks if a translation for a story is pending

    Args:
        story_id (int)
    Returns:
        boolean
    """
    return db.translations.find_one({'story_id': story_id}) is not None

WAITING_STATUS = 'waiting'
COMPLETE_STATUS = 'complete'

def get_waiting_translations():
    """ Gets all waiting translations

    Returns:
        :obj:`pymongo.Cursor`
    """
    return db.translations.find({
        'status': WAITING_STATUS
    })

def add_waiting_translation(uid, story_id):
    """ Add a translation as pending

    Args:
        uid (str)
        story_id (int)
    """
    db.translations.insert_one({
        'uid': uid,
        'story_id': story_id,
        'status': WAITING_STATUS
    })

def complete_translation(translation_uid, story):
    """ Marks a pending translation as complete and
        updates the parent story with the translation

    Args:
        translation_uid (str): the uid of the translation
        story (Story): the translation as a story, this will be
            added to the list of translations of the parent story
    """
    db.translations.update_one({
        'uid': translation_uid
    }, {'$set': {'status': COMPLETE_STATUS}})

    parent_story_id = db.translations.find_one({'uid': translation_uid})['story_id']
    parent_story = find_story(parent_story_id)
    parent_story.translations.append(story)
    update_story(parent_story)

def get_waiting_translation(translation_uid):
    """ Gets pending translations

    Args:
        translation_uid (str): uid of the translation
    Returns:
        dict: record of the translation
    """
    return db.translations.find_one({'uid': translation_uid})
