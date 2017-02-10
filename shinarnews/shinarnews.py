from flask import Flask, request, render_template

STORIES_PER_PAGE = 10

app = Flask(__name__)
# TODO
# app.config.from_object(__name__)
# app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

class Story:
    def __init__(self, title, link, lang, translations):
        self.title = title
        self.link = link
        self.lang = lang
        self.translations = translations


FAKE_DATA = [
        Story('pfSense: Open source network firewall distribution', 'https://pfsense.org/', 'en_us', [
            Story('pfSense: Open source network firewall distribution', None, 'pt_pt', [])
            ]),
        Story('Finland\'s Largest Trade Union Slams Basic Income as ‘Useless’ ', 'https://www.bloomberg.com/news/articles/2017-02-08/-useless-basic-income-trial-fails-test-at-biggest-finnish-union', 'en_us', []),
        Story('How the Flash Crash Trader’s $50M Fortune Vanished', 'https://www.bloomberg.com/news/features/2017-02-10/how-the-flash-crash-trader-s-50-million-fortune-vanished', 'en_us', []),
        ]


@app.route('/')
def stories():
    """ Shows the stories on HackerNews
    """

    return render_template('top.html', stories=FAKE_DATA)


if __name__ == '__main__':
    app.run(debug=True)
