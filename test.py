from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

result = sentiment_pipeline("I love this product!")
print(result)
