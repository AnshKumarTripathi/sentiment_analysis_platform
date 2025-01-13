from flask import Flask, render_template, request
import tweepy
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import config
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Authenticate to Twitter using the Bearer token
client = tweepy.Client(bearer_token=config.TWITTER_BEARER_TOKEN)

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        tweet_text = tweet.text
        sentiment = sentiment_pipeline(tweet_text)
        print(f"Tweet: {tweet_text}")
        print(f"Sentiment: {sentiment}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-stream', methods=['POST'])
def start_stream():
    keyword = request.form['keyword']
    logging.debug(f"Bearer Token: {config.TWITTER_BEARER_TOKEN}")
    logging.debug(f"Keyword: {keyword}")
    try:
        stream_listener = MyStreamListener(bearer_token=config.TWITTER_BEARER_TOKEN)
        stream_listener.add_rules(tweepy.StreamRule(keyword))
        stream_listener.filter()
        return f"Started streaming tweets for keyword: {keyword}"
    except tweepy.errors.Forbidden as e:
        logging.error("Forbidden - Check your API credentials and project settings.")
        return "Error: Forbidden - Check your API credentials and project settings."
    except tweepy.errors.TooManyRequests as e:
        logging.error("Rate limit exceeded. Please wait and try again later.")
        return "Rate limit exceeded. Please wait and try again later."

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    text = request.form['text']
    sentiment = sentiment_pipeline(text)
    return render_template('result.html', text=text, sentiment=sentiment)

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    url = request.form['url']
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save the fetched HTML content into a file for debugging
        with open('fetched_html.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        # Extract the main content based on common HTML structures
        text = soup.get_text(separator=' ', strip=True)
        
        # Save the fetched text content into a file for debugging
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        
        logging.debug(f"Scraped content: {text}")

        if not text or text.strip() == url:
            logging.error("No meaningful text found in the URL.")
            return "No meaningful content found to analyze."

        sentiment = sentiment_pipeline(text)
        return render_template('result.html', text=text, sentiment=sentiment)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while fetching the URL content."

if __name__ == '__main__':
    app.run(debug=True)
