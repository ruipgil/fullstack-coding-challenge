class Story:
    def __init__(self, title, link, author, lang="en", translations=None):
        self.title = title
        self.link = link
        self.author = author
        self.lang = lang
        if translations is None:
            self.translations = []
        else:
            self.translations = translations

    @staticmethod
    def from_json(json):
        if json['type'] == 'story':
            return Story(json['title'], json['url'], json['by'])
        return None
