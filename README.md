# Summary
This tool was designed to allow for sentiment analysis of news websites to determine if there was a potential sentiment coming through in the article text. Included in this repository is an example created for Al Jazeera.

# Use
Because this project makes use of the [Google Cloud Natural Language API](https://cloud.google.com/natural-language/), you will need to follow the GCP Console porject setup guide to acquire a private key. Once you have downloaded this key, place it inside of the `./creds` folder and title it `Google_App_Credentials.json`. You are now all set and ready to use the Al Jazeera implemention, or move on to creating your own implementation!

To use the Al Jazeera example implementation, simply run `./al_jazeera_scrape.py -h` to see command usage. I personally recommend running `./al_jazeera_scrape.py -f opinion_articles/articles_list.txt -o news_articles` for interesting results.

# Creating Another Implementation
Simply follow the example set by the Al Jazeera scraper in `al_jazeera_scrape.py`. All you need to do is implement your own arg parsing (or simply copy from the Al Jazeera example), a main function, and a scraper callback function using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). Refer to `al_jazeera_scrape.py` for reference.
