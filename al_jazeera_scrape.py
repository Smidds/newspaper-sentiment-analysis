#!/home/isaac/.local/share/virtualenvs/al-jazeera-analysis-bQZ22s6r/bin/python

import argparse
from web_scraper import Article, scrape_to_json
from sentiment import analyze
from bs4 import BeautifulSoup

def main():
    args = arg_parse()
    infile = args.file
    links = args.links
    outdir = args.output_dir

    outfile = scrape_to_json(infile, outdir, links, scraper)
    analyze(outfile)

def scraper(html, url):
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

    return Article(title, date, author, text, url)


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
                        default='news_articles',
                        help='The directory to output JSON-ified articles to {default is "news_articles"')
                        
    return parser.parse_args()

if __name__ == "__main__":
    main()