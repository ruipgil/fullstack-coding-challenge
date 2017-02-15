import os
import threading
import db
from flask import Flask, request, render_template, jsonify
from hn import top_stories, get_item_details
from translation import request_translate_stories, translation_updater

STORIES_PER_PAGE = 10
HN_UPDATE_INTERVAL = 30
TARGET_LANGUAGES = ['pt', 'it']

app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

def get_top_stories():
    """ Gets the current list of top stories, saves it,
        and retrieves them

    Returns:
        list of :obj:`Story`
    """
    stories_ids = top_stories(STORIES_PER_PAGE)
    db.save_top_stories(stories_ids)

    return retrieve_stories(stories_ids)

def retrieve_stories(stories_ids):
    """ Maps stories ids to story instances.
        It first looks in the database, if a story doesn't
        exist yet, it calls the HN API for the details about
        a story.

    Args:
        stories_ids (list of int)
    Returns:
        list of :obj:`Story`
    """
    stories = []
    stories_to_translate = []
    for story_id in stories_ids:
        cached_story = db.find_story(story_id)
        if cached_story is None:
            story = get_item_details(story_id)

            if not db.has_translation_waiting(story_id):
                stories_to_translate.append(story)

            db.save_story(story)
        else:
            story = cached_story
        stories.append(story)

    request_translate_stories(stories_to_translate, TARGET_LANGUAGES)

    return stories


@app.route('/')
def html_stories():
    """ Renders the top stories on HackerNews as HTML
    """
    stories = retrieve_stories(db.previous_top_stories())
    return render_template('top.html', stories=stories, translation_languages=TARGET_LANGUAGES)

@app.route('/.json')
def json_stories():
    """ Sends the current top stories JSON encoded
    """
    stories = retrieve_stories(db.previous_top_stories())
    return jsonify([story.to_json() for story in stories])

def stories_updater():
    """ Updates the stories in regular periods of time.
        Executes in a separate thread.
    """
    get_top_stories()
    translation_updater()
    threading.Timer(HN_UPDATE_INTERVAL, stories_updater).start()
threading.Timer(0, stories_updater).start()

if __name__ == '__main__':
    app.run(debug=True)
