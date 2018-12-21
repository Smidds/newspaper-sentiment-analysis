#!/home/isaac/.local/share/virtualenvs/al-jazeera-analysis-bQZ22s6r/bin/python

# System imports
import requests, sys, argparse
from os import getcwd
from os import listdir
from os import environ
from os.path import isfile, join
from web_scraper import Article, JSON_to_articles
from colorama import Fore, Back, Style

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
   total_score = 0
   total_magnitude = 0

   for article in articles:
      print '"{}"'.format(Fore.CYAN + Style.BRIGHT + article.title + Fore.RESET + Style.RESET_ALL)
      if (len(article.url) != 0):
         print 'URL: {}'.format(article.url)
      print 'Author: {}\nDate: {}'.format(article.author, article.date)

      # The text to analyze
      document = types.Document(
         content=article.text,
         type=enums.Document.Type.PLAIN_TEXT)

      # Detects the sentiment of the text
      annotations = client.analyze_sentiment(document=document, encoding_type='UTF32')
      sentiment = annotations.document_sentiment

      total_score += sentiment.score
      total_magnitude += sentiment.magnitude

      sentiment_score_text = ""
      if sentiment.score > 0:
         sentiment_score_text = '{}{}{}'.format(Fore.GREEN, sentiment.score, Fore.RESET)
      elif sentiment.score < 0:
         sentiment_score_text = '{}{}{}'.format(Fore.RED, sentiment.score, Fore.RESET)
      else:
         sentiment_score_text = sentiment.score

      sentiment_magnitude_text = ""
      if sentiment.magnitude >= 5:
         sentiment_magnitude_text = '{}{}{}'.format(Fore.YELLOW, sentiment.magnitude, Fore.RESET)
      else:
         sentiment_magnitude_text = sentiment.magnitude

      print Fore.BLUE + Style.BRIGHT + '  Overal Sentiment:' + Fore.RESET + Style.RESET_ALL
      print ('     Score: ' + Style.BRIGHT + '{}' + Style.RESET_ALL + ', Magnitude: ' + Style.BRIGHT + '{}' + Style.RESET_ALL).format(sentiment_score_text, sentiment_magnitude_text)
      print ''
      print ''

   avg_score = total_score / len(articles)
   avg_magnitude = total_magnitude / len(articles)
   avg_score_text = ''

   if avg_score > 0:
      avg_score_text = '{}{}{}'.format(Fore.GREEN, avg_score, Fore.RESET)
   elif avg_score < 0:
      avg_score_text = '{}{}{}'.format(Fore.RED, avg_score, Fore.RESET)
   else:
      avg_score_text = avg_score

   avg_magnitude_text = ""
   if avg_magnitude >= 5:
      avg_magnitude_text = '{}{}{}'.format(Fore.YELLOW, avg_magnitude, Fore.RESET)
   else:
      avg_magnitude_text = avg_magnitude

   print '=========== [ Total Results ] ==========='
   print 'Average Score: {}'.format(avg_score_text)
   print 'Average Magnitude: {}'.format(avg_magnitude_text)