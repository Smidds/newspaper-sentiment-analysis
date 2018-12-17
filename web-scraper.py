#!/home/isaac/.local/share/virtualenvs/al-jazeera-analysis-bQZ22s6r/bin/python

# import libraries
import sys, argparse
import json
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def main():
    args = arg_parse()

    if args.file != None:
        f = open(args.file, 'r')
        args.links += f.read().splitlines()

    for url in args.links:
        html = BeautifulSoup(simple_get(url), 'html.parser')
        if html == None:
            exit(2)

        author = ''
        text = ''
        title = ''
        date = ''

        title = html.title.string
        
        date_elem = html.find_all('time', {'class' : 'timeagofunction'}).pop()
        if date_elem != None:
            date = date_elem.attrs['datetime']
        
        author_div_elem = html.find_all('div', {'class' : 'article-heading-author-name'}).pop()
        if author_div_elem != None:
            author_span = author_div_elem.find('span')
            if author_span != None:
                author_a = author_span.find('a')
                if author_a != None:
                    author = author_a.get_text()

        if author == '':
            source_div_elem = html.find('div', {'class' : 'article-body-artSource'})
            if source_div_elem != None:
                source_p = source_div_elem.find('p')
                if source_p != None:
                    source_span = source_p.find('span')
                    if source_span != None:
                        author = source_span.get_text()

        outer_div = html.find_all('div', 'article-p-wrapper')
        for element in outer_div:
            paragraphs = element.find_all('p')
            for p in paragraphs:
                text += u''.join((p.get_text())).encode('utf-8')

        story = Article(title, date, author, text)

        story_json = json.dumps(story.__dict__) 
        f = open("{}/{}".format(args.output_dir, story.title), 'w')
        f.write(story_json)
        f.close()


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


def arg_parse():
    parser = argparse.ArgumentParser(description='Scrape from the provided Al Jazeera link.')
    parser.add_argument('links', 
                        metavar='URL', 
                        help='Link(s) to pull from',
                        default=[],
                        nargs='*')
    parser.add_argument('-f', 
                        metavar='FILE', 
                        dest='file',
                        help='File containing a list of links seperated by a newline')
    parser.add_argument('-o',
                        metavar='DIR',
                        dest='output_dir',
                        default='',
                        help='The directory to output JSON-ified articles to')
                        
    return parser.parse_args()

if __name__ == "__main__":
    main()