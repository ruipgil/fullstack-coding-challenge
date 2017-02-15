class Story:
    def __init__(self, id, title, link, author, lang="en", translations=None):
        self.id = id
        self.title = title
        self.link = link
        self.author = author
        self.lang = lang

        if translations is None:
            self.translations = {}
        else:
            self.translations = translations

    def translate(self, target_lang):
        return

    def to_json(self):
        return {
                'id': self.id,
                'title': self.title,
                'link': self.link,
                'author': self.author,
                'lang': self.lang,
                'translations': self.translations
                }

    @staticmethod
    def from_json(json):
        if json['type'] == 'story' or json['type'] == 'job':
            return Story(json['id'], json['title'], json.get('url', ''), json['by'], json.get('translations', {}))
        return None

    @staticmethod
    def from_db(story):
        return Story(
            story['id'],
            story['title'],
            story['link'],
            story['author'],
            story['lang'],
            story['translations']
        )
