from transformers import pipeline

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Example usage
result = sentiment_pipeline("I love this product!")
print(result)
