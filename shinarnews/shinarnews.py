from flask import Flask, request, render_template
from hn import top_stories, get_item_details

STORIES_PER_PAGE = 10

app = Flask(__name__)
# TODO
# app.config.from_object(__name__)
# app.config.from_envvar('MINITWIT_SETTINGS', silent=True)


@app.route('/')
def stories():
    """ Shows the stories on HackerNews
    """
    stories = [get_item_details(story) for story in top_stories(STORIES_PER_PAGE)]

    return render_template('top.html', stories=stories)


if __name__ == '__main__':
    app.run(debug=True)
