from flask import Flask, request, render_template
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

_previous_stories = []

def get_stories():
    global _previous_stories
    stories_ids = top_stories(STORIES_PER_PAGE)
    _previous_stories = stories_ids

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

def has_changed():
    global _previous_stories
    stories_ids = top_stories(STORIES_PER_PAGE)

    if set(stories_ids) != set(_previous_stories):
        _previous_stories = stories_ids
        # TODO: async!
        # get_stories()
        return False
    else:
        return True


@app.route('/')
def stories():
    """ Shows the stories on HackerNews
    """

    return render_template('top.html', stories=retrieve_stories(_previous_stories))


# timer that each XX seconds checks for new data

import threading
get_stories()
threading.Timer(20, get_stories).start()



if __name__ == '__main__':
    app.run(debug=True)
