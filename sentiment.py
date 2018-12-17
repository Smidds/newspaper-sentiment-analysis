#!/home/isaac/.local/share/virtualenvs/al-jazeera-analysis-bQZ22s6r/bin/python

# System imports
import requests, sys, argparse
from os import getcwd
from os import listdir
from os import environ
from os.path import isfile, join
from web_scraper import Article, JSON_to_articles

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def analyze(articles_file):
   environ['GOOGLE_APPLICATION_CREDENTIALS'] = getcwd() + "/creds/Google_App_Credentials.json"

   # Instantiates a client
   client = language.LanguageServiceClient()

   articles_json = open(articles_file, 'r').read()
   articles = JSON_to_articles(articles_json)

   for article in articles:
      print '"{}"'.format(bcolors.HEADER + bcolors.UNDERLINE + article.title + bcolors.ENDC)
      # The text to analyze
      document = types.Document(
         content=article.text,
         type=enums.Document.Type.PLAIN_TEXT)

      # Detects the sentiment of the text
      annotations = client.analyze_sentiment(document=document, encoding_type='UTF32')
      sentiment = annotations.document_sentiment

      sentiment_score_text = ""
      if sentiment.score > 0:
         sentiment_score_text = '{}{}{}'.format(bcolors.OKGREEN, sentiment.score, bcolors.ENDC)
      elif sentiment.score < 0:
         sentiment_score_text = '{}{}{}'.format(bcolors.FAIL, sentiment.score, bcolors.ENDC)
      else:
         sentiment_score_text = sentiment.score

      sentiment_magnitude_text = ""
      if sentiment.magnitude >= 5:
         sentiment_magnitude_text = '{}{}{}'.format(bcolors.WARNING, sentiment.magnitude, bcolors.ENDC)
      else:
         sentiment_magnitude_text = sentiment.magnitude

      print 'Author: {}\nDate: {}'.format(article.author, article.date)
      print bcolors.OKBLUE + bcolors.BOLD + '  Overal Sentiment:' + bcolors.ENDC
      print '     Score: {}, Magnitude: {}'.format(sentiment_score_text, sentiment_magnitude_text)
      print ''
      print ''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'