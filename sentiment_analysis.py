from transformers import pipeline

sentiment = pipeline("sentiment-analysis")
result1 = sentiment("I love AI!")
result2 = sentiment("I hate AI!")
print(result1)
print(result2)
# [{'label': 'POSITIVE', 'score': 0.9998}]
