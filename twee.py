import tweepy
import config

client = tweepy.Client(bearer_token=config.TWITTER_BEARER_TOKEN)

# Test fetching recent tweets with the corrected max_results value
try:
    response = client.search_recent_tweets(query="JavaScript", max_results=10)  # Set max_results between 10 and 100
    for tweet in response.data:
        print(tweet.text)
except tweepy.errors.Forbidden as e:
    print("Error: Forbidden - Check your API credentials and project settings.")
except Exception as e:
    print(f"An error occurred: {e}")
