import os
import unittest
import tempfile
import shinarnews.db as db
from shinarnews.Story import Story
from shinarnews.shinarnews import STORIES_PER_PAGE

def date(s):
    return s

class TestDB(unittest.TestCase):
    def tearDown(self):
        db.db.top_stories.delete_many({})
        db.db.stories.delete_many({})
        db.db.translations.delete_many({})

    def setUp(self):
        self.tearDown()
        db._use_test()
        db.db.top_stories.insert_many([{"top" : [13653669, 13653819, 13653383, 13652093, 13653079, 13652153, 13652612, 13651947, 13652094, 13653826]}])
        db.db.stories.insert_many([
            {"id" : 13653383, "author" : "rodionos", "link" : "https://github.com/axibase/atsd-use-cases/blob/master/OrovilleDam/README.md", "title" : "Will the Oroville Dam survive the upcoming rain?", "lang" : {  }, "translations" : { "it" : "Sarà la diga di Oroville sopravvivere la pioggia imminente?", "pt" : "Será que o Oroville Dam sobreviver a próxima chuva?" }},
            { "id" : 13652093, "author" : "spaceboy", "link" : "https://securedrop.org/", "title" : "SecureDrop – An open-source whistleblower submission system", "lang" : {  }, "translations" : { "it" : "SecureDrop - Un sistema di informatore presentazione open-source", "pt" : "Securedrop - Um sistema de submissão denunciante open-source" } },
            { "id" : 13652153, "author" : "axiom", "link" : "https://www.bloomberg.com/news/articles/2017-02-15/top-hat-raises-22-5-million-to-go-after-pearson-mcgraw-hill", "title" : "Top Hat Raises $22M to Go After Pearson, McGraw-Hill", "lang" : {  }, "translations" : { "it" : "Cappello a cilindro solleva $ 22M per andare dopo Pearson, McGraw-Hill", "pt" : "Top Hat levanta $ 22M para ir atrás de Pearson, McGraw-Hill" } },
            { "id" : 13653079, "author" : "richardboegli", "link" : "http://www.bloomberg.com/news/articles/2017-02-15/verizon-reduces-yahoo-deal-price-by-250-million-in-revised-deal", "title" : "Verizon Reduces Yahoo Deal Price by $250 Million in Revised Deal", "lang" : {  }, "translations" : { "it" : "Verizon riduce Yahoo Deal prezzo da $ 250 milioni a Deal Revised", "pt" : "Verizon Reduz Yahoo negócio preço em US $ 250 milhões em Deal Revised" } },
            { "id" : 13652094, "author" : "mnoeld", "link" : "http://www.theverge.com/2017/2/15/14622074/microsoft-aerial-informatics-and-robotics-platform", "title" : "Microsoft lets you crash drones and robots in its new real world simulator", "lang" : {  }, "translations" : { "it" : "Microsoft consente di droni e robot di crash nel suo nuovo simulatore mondo reale", "pt" : "Microsoft permite-lhe drones acidente e robôs em seu novo simulador do mundo real" } },
            { "id" : 13647098, "author" : "benbreen", "link" : "http://blissbat.net/balzac.html", "title" : "The Pleasures and Pains of Coffee (1830)", "lang" : {  }, "translations" : { "it" : "I piaceri ei dolori di caffè (1830)", "pt" : "Os prazeres e as dores de Café (1830)" } },
            { "id" : 13651947, "author" : "daegloe", "link" : "http://news.mit.edu/2017/dataset-nearby-stars-available-public-exoplanets-0213", "title" : "Scientists make huge dataset of nearby stars available to public", "lang" : {  }, "translations" : { "it" : "Gli scienziati fanno enormi set di dati di stelle vicine a disposizione del pubblico", "pt" : "Cientistas fazem enorme conjunto de dados de estrelas próximas disponível ao público" } },
            { "id" : 13652111, "author" : "spaceboy", "link" : "https://www.strongswan.org/", "title" : "StrongSwan – IPsec VPN for Linux, Android, FreeBSD, Mac OS X, Windows", "lang" : {  }, "translations" : { "it" : "StrongSwan - IPsec VPN per Linux, Android, FreeBSD, Mac OS X, Windows", "pt" : "StrongSwan - IPsec VPN para Linux, Android, FreeBSD, Mac OS X, Windows" } },
            { "id" : 13647279, "author" : "shiftb", "link" : "https://tech.instacart.com/the-garden-instacarts-physical-staging-environment-7204fd063616", "title" : "The Garden: Instacart's Physical Staging Environment", "lang" : {  }, "translations" : { "it" : "Il Giardino: ambiente di staging fisica di Instacart", "pt" : "O Jardim: de Instacart Staging Ambiente Físico" } },
            { "id" : 13652541, "author" : "nirvdrum", "link" : "http://nirvdrum.com/2017/02/15/truffleruby-on-the-substrate-vm.html", "title" : "TruffleRuby on the Substrate VM", "lang" : {  }, "translations" : { "it" : "TruffleRuby sul substrato VM", "pt" : "TruffleRuby sobre o substrato VM" } },
            { "title" : "Algorithms and Data Structures (Khan Academy)", "lang" : {  }, "id" : 13653669, "link" : "https://www.khanacademy.org/computing/computer-science/algorithms/", "translations" : {  }, "author" : "rsandhu" },
            { "title" : "TensorFlow 1.0 Released", "lang" : {  }, "id" : 13653819, "link" : "https://www.tensorflow.org/", "translations" : {  }, "author" : "plexicle" },
            { "title" : "Someone Stole My Startup Idea, and Why It Doesn't Matter", "lang" : {  }, "id" : 13652612, "link" : "https://blog.nugget.one/upstart/someone-stole-my-startup-idea-and-why-it-doesnt-matter/", "translations" : {  }, "author" : "jv22222" },
            { "link" : "https://github.com/tensorflow/tensorflow/releases/tag/v1.0.0", "id" : 13653826, "translations" : {  }, "title" : "TensorFlow 1.0.0 released", "author" : "runesoerensen", "lang" : {  } }
        ])
        db.db.translations.insert_many([
            { "time" : date("2017-02-15T17:40:34.925Z"), "target_language" : "it", "uid" : "28a33f4075", "story_id" : 13651947, "status" : db.WAITING_STATUS },
            { "time" : date("2017-02-15T17:40:35.540Z"), "target_language" : "pt", "uid" : "0abc49646c", "story_id" : 13652111, "status" : "complete" },
            { "time" : date("2017-02-15T17:40:36.154Z"), "target_language" : "it", "uid" : "0aee1fd200", "story_id" : 13652111, "status" : "complete" },
            { "time" : date("2017-02-15T17:40:36.768Z"), "target_language" : "pt", "uid" : "9060f5562f", "story_id" : 13647279, "status" : "complete" },
            { "time" : date("2017-02-15T17:40:37.383Z"), "target_language" : "it", "uid" : "d98ebcd85e", "story_id" : 13647279, "status" : "complete" },
            { "time" : date("2017-02-15T17:40:37.997Z"), "target_language" : "pt", "uid" : "8f220f3244", "story_id" : 13652541, "status" : "complete" },
            { "time" : date("2017-02-15T17:40:38.612Z"), "target_language" : "it", "uid" : "eae136c362", "story_id" : 13652541, "status" : "complete" }
        ])

    def test_previous_top_stories(self):
        stories = db.previous_top_stories()
        self.assertTrue(isinstance(stories, list))
        self.assertEqual(len(stories), STORIES_PER_PAGE)
        for story in stories:
            self.assertTrue(isinstance(story, int))

    def test_save_top_stories(self):
        stories = [1, 2, 3, 4, 5, 6, 7, 8, 0, 10]
        db.save_top_stories(stories)
        self.assertEqual(db.db.top_stories.count(), 1)

    def test_find_story(self):
        story = db.find_story(13653383)
        self.assertTrue(isinstance(story, Story))
        self.assertEqual(story.title, 'Will the Oroville Dam survive the upcoming rain?')

        story = db.find_story(2)
        self.assertTrue(story is None)

    def test_update_story(self):
        story = db.find_story(13653383)
        story.title = '?'
        db.update_story(story)
        self.assertEqual(db.db.stories.find({'id': 13653383}).count(), 1)

        story = db.find_story(13653383)
        self.assertEqual(story.title, '?')

    def test_has_translation_waiting(self):
        story_id = 13651947
        self.assertTrue(db.has_translation_waiting(story_id))
        self.assertFalse(db.has_translation_waiting(200))

    def test_get_waiting_translations(self):
        story_id = 13651947
        waiting = db.get_waiting_translations()
        self.assertEqual(waiting.count(), 1)
        for w in waiting:
            self.assertEqual(w['story_id'], story_id)

    def test_add_waiting_translation(self):
        previous_count = db.db.translations.find().count()
        previous_waiting_count = db.get_waiting_translations().count()

        uid = 198
        lang = 'ch'
        story_id = 9379
        db.add_waiting_translation(uid, story_id, lang)

        self.assertEqual(previous_count+1, db.db.translations.find().count())
        self.assertEqual(previous_waiting_count+1, db.get_waiting_translations().count())

        translation = db.db.translations.find_one({ 'uid': uid, 'story_id': story_id })
        self.assertTrue(translation is not None)
        self.assertEqual(set(dict(translation).keys()), set(['_id', 'uid', 'time', 'story_id', 'status', 'target_language']))
        self.assertEqual(translation['uid'], uid)
        self.assertEqual(translation['story_id'], story_id)
        self.assertEqual(translation['status'], db.WAITING_STATUS)
        self.assertEqual(translation['target_language'], lang)

    def test_complete_translation(self):
        story_id = 13651947
        uid = "28a33f4075"
        lang = 'ch'
        text = "This is not a real translation"

        previous_count = db.db.translations.find().count()
        db.complete_translation(uid, text, lang)
        self.assertEqual(previous_count, db.db.translations.find().count())
        translation = db.db.translations.find_one({ 'uid': uid, 'story_id': story_id })
        self.assertEqual(translation['status'], db.COMPLETE_STATUS)

        story = db.find_story(story_id)
        self.assertTrue(lang in story.translations.keys())

    def test_get_translations(self):
        translations = list(db.get_translations())
        self.assertEqual(translations[0]['uid'], "eae136c362")
        self.assertEqual(translations[-1]['uid'], "28a33f4075")

    def test_update_translation_status(self):
        uid = "eae136c362"
        status= "NO_STATUS"
        db.update_translation_status(uid, status)
        translation = db.db.translations.find_one({'uid': uid})
        self.assertEqual(translation['status'], status)

    def test_has_translation_in_process(self):
        lang = "it"
        story_id = 13651947
        self.assertTrue(db.has_translation_in_process(story_id, lang))
        self.assertFalse(db.has_translation_in_process(story_id, 'ru'))


if __name__ == '__main__':
    unittest.main()
