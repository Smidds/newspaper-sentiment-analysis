#!/home/isaac/.local/share/virtualenvs/al-jazeera-analysis-bQZ22s6r/bin/python

import sys, argparse, json, time
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def scrape_to_json(infile=None, outdir="", links=[], scraper=()):
    """Process the provided scraper callback, returns file we create.

    Given a file to attempt to grab links from and a links list, we iterate over them and 
    get the HTML and invoke the scraper callback. Then we print the JSON results and return the filename.
    """
    if infile != None:
        f = open(infile, 'r')
        links += f.read().splitlines()

    article_list = []

    for url in links:
        html = BeautifulSoup(simple_get(url), 'html.parser')
        if html == None:
            exit(2)

        story = scraper(html)

        if story != None:
            story.__type__ = "Article"
            article_list.append(story)

    filename = "{}/{}.json".format(outdir, time.strftime("%d-%m-%y_%H:%M:%S"))
    f = open(filename, 'w')
    article_list_json = json.dumps([article.__dict__ for article in article_list])
    f.write(article_list_json)
    f.close()
    return filename

def article_object_parser(obj):
    if '__type__' in obj and obj['__type__'] == 'Article':
        return Article(obj['title'], obj['date'], obj['author'], obj['text'])
    return None

def JSON_to_articles(article_json):
    article = json.loads(article_json, object_hook=article_object_parser)
    return article

class Article:
    title = ""
    date = ""
    author = ""
    text = ""

    def __init__(self, title, date, author, text):
        self.title = title
        self.date = date
        self.author = author
        self.text = text

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)