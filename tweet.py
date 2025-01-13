import tweepy
import config

def fetch_tweets(keyword):
    client = tweepy.Client(bearer_token=config.TWITTER_BEARER_TOKEN)
    try:
        response = client.search_recent_tweets(query=keyword, max_results=10)  # Adjust max_results as needed
        return [tweet.text for tweet in response.data]
    except tweepy.errors.Forbidden as e:
        return f"Error: Forbidden - Check your API credentials and project settings."
    except Exception as e:
        return f"An error occurred: {e}"
