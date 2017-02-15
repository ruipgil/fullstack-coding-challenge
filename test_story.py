import os
import unittest
from shinarnews.Story import Story

story_id = 8
title = 'A simple and testing title'
link = 'http://example.com'
author = 'ruipgil'
lang = 'pt'
translations = {
    'en': 'Bad translation',
    'it': 'This is only a test'
}

class TestStory(unittest.TestCase):
    def setUp(self):
        self.story_template = Story(story_id, title, link, author, lang, translations)

    def test_init(self):
        story = self.story_template
        self.assertEqual(story.id, story_id)
        self.assertEqual(story.title, title)
        self.assertEqual(story.link, link)
        self.assertEqual(story.author, author)
        self.assertEqual(story.lang, lang)
        self.assertEqual(story.translations, translations)

        story = Story(story_id, title, link, author, lang)
        self.assertEqual(story.id, story_id)
        self.assertEqual(story.title, title)
        self.assertEqual(story.link, link)
        self.assertEqual(story.author, author)
        self.assertEqual(story.lang, lang)
        self.assertEqual(story.translations, {})

        story = Story(story_id, title, link, author)
        self.assertEqual(story.id, story_id)
        self.assertEqual(story.title, title)
        self.assertEqual(story.link, link)
        self.assertEqual(story.author, author)
        self.assertEqual(story.lang, 'en')
        self.assertEqual(story.translations, {})

    def test_to_json(self):
        json = self.story_template.to_json()

        self.assertTrue(isinstance(json, dict))
        self.assertEqual(set(json.keys()), set(['id', 'title', 'link', 'author', 'lang', 'translations']))
        self.assertTrue(isinstance(json['id'], int))
        self.assertTrue(isinstance(json['title'], str))
        self.assertTrue(isinstance(json['link'], str))
        self.assertTrue(isinstance(json['author'], str))
        self.assertTrue(isinstance(json['lang'], str))
        self.assertTrue(isinstance(json['translations'], dict))
        self.assertEqual(set(json['translations'].keys()), set(['en', 'it']))
        for val in json['translations'].values():
            self.assertTrue(isinstance(val, str))

    def test_from_json(self):
        json = {
            'type': 'bad_type'
        }
        self.assertTrue(Story.from_json(json) is None)

        json = {
            'type': 'story',
            'id': story_id,
            'title': title,
            'by': ''
        }
        sto = Story.from_json(json)
        self.assertTrue(isinstance(sto, Story))
        self.assertEqual(sto.link, '')
        self.assertEqual(set(sto.translations.keys()), set([]))

    def test_from_db(self):
        db = {
            'id': 937,
            'title': 'a tt',
            'link': 'unbabel.com',
            'author': 'ruipgil',
            'lang': 'pt',
            'translations': {
                'en': 'What?'
            }
        }
        story = Story.from_db(db)
        self.assertTrue(isinstance(story, Story))
        self.assertEqual(story.link, db['link'])

if __name__ == '__main__':
    unittest.main()
