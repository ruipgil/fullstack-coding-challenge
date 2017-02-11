from flask import Flask, request, render_template, jsonify
from Story import Story
from hn import top_stories, get_item_details
from pymongo import MongoClient

STORIES_PER_PAGE = 10

app = Flask(__name__)
# TODO
# app.config.from_object(__name__)
# app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

# TODO: Change to env variables
client = MongoClient('localhost', 32768)
mongo = client.test
""" Database structure:
    stories: [{ id, title, author, ... }]
    top_stories: [{ top: [] }] #only one record
"""


def previous_top():
    tops = mongo.top_stories.find_one()
    return tops['top'] if tops is not None else []

def save_top(tops):
    if mongo.top_stories.count() == 0:
        mongo.top_stories.insert_one({'top': tops})
    else:
        mongo.top_stories.update_one({}, {'$set': {'top': tops}})

def get_stories():
    stories_ids = top_stories(STORIES_PER_PAGE)
    save_top(stories_ids)

    return retrieve_stories(stories_ids)

def retrieve_stories(stories_ids):
    _stories = []
    for story_id in stories_ids:
        m_stories = mongo.stories
        cached_story = m_stories.find_one({'id': story_id})
        if cached_story is None:
            story = get_item_details(story_id)
            story.save(mongo)
        else:
            story = Story.from_db(cached_story)
        _stories.append(story)

    return _stories

@app.route('/')
def stories():
    """ Shows the stories on HackerNews
    """

    return render_template('top.html', stories=retrieve_stories(previous_top()))

@app.route('/.json')
def json_stories():
    return jsonify([story.to_json() for story in retrieve_stories(previous_top())])

# timer that checks for new data each XX seconds
import threading
get_stories()
threading.Timer(20, get_stories).start()

if __name__ == '__main__':
    app.run(debug=True)
