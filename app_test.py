from flask import Flask, render_template, request
from transformers import pipeline
from tweet import fetch_tweets  # Import the standalone script function
from scrape_url import scrape_url_content  # Import the scrape_url_content function
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-stream', methods=['POST'])
def start_stream():
    keyword = request.form['keyword']
    logging.debug(f"Keyword: {keyword}")
    tweets = fetch_tweets(keyword)
    if isinstance(tweets, str):
        return tweets  # Return error message if there's an issue with the API request
    results = [(tweet, sentiment_pipeline(tweet)) for tweet in tweets]
    return render_template('result.html', keyword=keyword, results=results)

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    text = request.form['text']
    sentiment = sentiment_pipeline(text)
    return render_template('result_text.html', text=text, sentiment=sentiment)

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    url = request.form['url']
    text = scrape_url_content(url)
    if "An error occurred" in text:
        return text  # Return error message if there's an issue with scraping
    
    # Tokenize text and take the first 512 tokens
    tokenizer = sentiment_pipeline.tokenizer
    inputs = tokenizer(text, truncation=True, max_length=512, return_tensors='pt')
    
    # Convert tokens back to text
    truncated_text = tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True)
    
    # Analyze sentiment of truncated text
    sentiment = sentiment_pipeline(truncated_text)
    
    return render_template('result_url.html', text=truncated_text, sentiment=sentiment, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
