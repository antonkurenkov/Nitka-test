from flask import request, render_template
from app import app

import requests
import re


@app.route('/index')
@app.route('/')
def my_form():
    """Returns default form for the index page."""
    return render_template('index.html')


@app.route('/index', methods=['POST'])
@app.route('/', methods=['POST'])
def main_form_post():
    """
    Returns a rendered page depends on type of API response.

    Keyword arguments:

    * title - the title of the page to load.
    """
    text = request.form['text']
    params = {
        "action": "query",
        "format": "json",
        "titles": text,
        "prop": "pageprops",
        "redirects": True,
    }
    response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
    data = response.json()
    pageid = list(data['query']['pages'].keys())[0]
    if pageid != '-1':
        hasprops = True if 'pageprops' in list(data['query']['pages'][pageid]) else False
        if hasprops and list(data['query']['pages'][pageid]['pageprops'].keys())[0] == 'disambiguation':
            refers = get_links(text)
            return render_template('refers.html', refers=refers, title=text)
        else:
            description = get_description(text)
            image = get_image(text)
            return render_template('article.html', image=image, alt=description, title=text)
    else:
        return render_template('empty.html', alt='term not found', title=text)


def get_description(title):
    """
    Get short description given article.
    Returns a string of page description.
    If description is absent for the page, takes the first sentence of the article summary.

    Keyword arguments:

    * title - the title of the page to load.
    """
    try:
        params = {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "titles": title,
            "prop": "description",
            "redirects": True,
        }
        response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
        data = response.json()
        return data["query"]["pages"][0]["description"].capitalize() + '.'
    except KeyError:
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            'prop': 'extracts',
            'explaintext': True,
            'redirects': True,
        }
        response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
        data = response.json()
        return list(data["query"]["pages"].values())[0]['extract'].partition('.')[0] + '.'


def get_image(title):
    """
    Get a main image of a given article.
    Returns a direct image link or 'False' if image is not presented in the article.

    Keyword arguments:

    * title - the title of the page to load.
    """
    try:
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "pageimages",
            "piprop": "original",
            "redirects": True,
        }
        response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
        data = response.json()
        return list(data["query"]["pages"].values())[0]['original']['source']
    except KeyError:
        return False


def get_links(title):
    """
    Get a list of titles for requested query.
    The func finds all referred articles and returns the list of their titles.

    Keyword arguments:

    * title - the title of the page to load.
    """
    try:
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            'prop': 'revisions',
            'rvprop': 'content',
            "redirects": True,
        }
        response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
        data = response.json()
        refers = list(data["query"]["pages"].values())[0]['revisions'][0]['*']
        my_links = re.findall(r'\[\[(.*?)\]\]', refers)
        return [link.partition('|')[0] for link in my_links]
    except KeyError:
        return False
