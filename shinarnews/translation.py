import os
import json
import threading

import db
from Story import Story
from unbabel.api import UnbabelApi

TRANSLATION_CHECKING_INTERVAL = 20

api = UnbabelApi(
    username=os.environ.get('UNBABEL_USERNAME'),
    api_key=os.environ.get('UNBABEL_API_KEY'),
    sandbox=True
)

def request_translate_story(story, langs):
    """ Requests a story to be translated

    Args:
        story (:obj:`Story`)
        langs (list of str)
    """
    for lang in langs:
        try:
            translation = api.post_mt_translations(story.title, target_language=lang)
            db.add_waiting_translation(translation.uid, story.id)
        except Exception as err:
            print('Can\'t translate story %d: %s' % (story.id, err))

def request_translate_stories(stories, langs):
    """ Requests a series of stories to be translated to certain languages

    Args:
        stories (list of :obj:`Story`)
        langs (list of str): list of languages to translate to
    """
    for story in stories:
        request_translate_story(story, langs)

def translation_checker():
    """ Checks for pending translations regularly,
        in a separate thread
    """
    waiting = db.get_waiting_translations()
    for waiting_translation in waiting:
        uid = waiting_translation['uid']
        # try:
        translation = api.get_mt_translation(uid)
        if translation.status == 'deliver_ok':
            translated_text = translation.translation
            target_language = translation.target_language
            as_story = Story(None, translated_text, None, None, target_language)
            db.complete_translation(uid, as_story)
        # TODO more statuses

        # except Exception as err:
        #     print('Err: %s' % err)

    threading.Timer(TRANSLATION_CHECKING_INTERVAL, translation_checker).start()

translation_checker()
