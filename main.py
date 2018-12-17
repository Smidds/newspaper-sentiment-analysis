#!/home/isaac/.local/share/virtualenvs/al-jazeera-analysis-bQZ22s6r/bin/python

# System imports
import requests, sys, argparse
from os import getcwd
from os import listdir
from os import environ
from os.path import isfile, join

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def main():
   args = arg_parse()
   environ['GOOGLE_APPLICATION_CREDENTIALS'] = getcwd() + "/creds/Google_App_Credentials.json"

   # Instantiates a client
   client = language.LanguageServiceClient()

   files_in_directory = []
   if (args.articles == None):
      args.articles = []

   if (args.directories != None):
      for directory in args.directories:
         files_in_directory += [open('{}/{}'.format(directory, f), 'r') for f in listdir(directory) if isfile(join(directory, f))]

   args.articles += files_in_directory

   for article in args.articles:
      name = article.name
      index = name.rfind('/')
      if index != -1:
         name = name[index + 1:]


      print '"{}"'.format(bcolors.HEADER + bcolors.UNDERLINE + name + bcolors.ENDC)
      # The text to analyze
      text = article.read()
      document = types.Document(
         content=text,
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

def arg_parse():
   parser = argparse.ArgumentParser(epilog="""This program makes use of the Google sentiment analysis API for parsing text and analyizing sentiment.
                                             This should not be read as a replacement for actually reading the text and gathering your own analysis
                                             of sentiment as this technology is very much in its infancy and under development.
                                             
                                             Thanks! -The Developer""", 
                                    description='Gather sentiment analysis of provided text')
   parser.add_argument('-f', 
                        metavar='article', 
                        help='Files to process text from', 
                        nargs='+', 
                        dest='articles',
                        type=argparse.FileType('r'))
   parser.add_argument('-o',
                        metavar='FILE',
                        nargs='+', 
                        help='Files to output the results to',
                        type=argparse.FileType('w'),
                        default=sys.stdout)
   parser.add_argument('-d',
                        metavar='directory',
                        dest='directories',
                        help='Directory in which to find articles to parse',
                        nargs='+')

   return parser.parse_args()

if __name__ == "__main__":
   main()