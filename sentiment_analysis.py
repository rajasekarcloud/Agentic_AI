from transformers import pipeline
# Hugging Face Transformers, the pipeline will by default load the model:
# A DistilBERT model fine‑tuned on the Stanford Sentiment Treebank v2 (SST‑2) dataset.
# - It predicts positive or negative sentiment for English text.
sentiment = pipeline("sentiment-analysis")
result1 = sentiment("I love AI!")
result2 = sentiment("I hate AI!")
result3 = sentiment("I hate and love AI!")
print(result1)
print(result2)
print(result3)
[{'label': 'POSITIVE', 'score': 0.9998650550842285}]
[{'label': 'NEGATIVE', 'score': 0.9992353916168213}]
[{'label': 'POSITIVE', 'score': 0.9994539618492126}]

