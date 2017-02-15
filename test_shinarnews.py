import os
import unittest
import tempfile
import shinarnews.db as db
from shinarnews.Story import Story
from shinarnews.shinarnews import get_top_stories, retrieve_stories, STORIES_PER_PAGE

class TestShinarnews(unittest.TestCase):
    def test_get_top_stories(self):
        get_top_stories()
        top_stories = db.previous_top_stories()
        self.assertEqual(len(top_stories), STORIES_PER_PAGE)
        for story in top_stories:
            self.assertTrue(isinstance(story, int))

    def test_retrieve_stories(self):
        top_stories = db.previous_top_stories()
        stories = retrieve_stories(top_stories)
        self.assertTrue(isinstance(stories, list))
        self.assertEqual(len(stories), len(top_stories))
        for story in stories:
            self.assertTrue(isinstance(story, Story))


if __name__ == '__main__':
    unittest.main()
