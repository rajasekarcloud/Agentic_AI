#Sentiment vs Text Classification
from transformers import pipeline

# Example text
text = "I love working with AI tools, they make life so much easier!"

# Sentiment Analysis Pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
sentiment_result = sentiment_pipeline(text)

# Text Classification Pipeline (general-purpose)
# Using a model fine-tuned for sentiment as an example
text_classification_pipeline = pipeline(
    "text-classification", 
    model="bert-base-uncased-finetuned-sst-2-english"
)
text_classification_result = text_classification_pipeline(text)

# Print results
print("=== Sentiment Analysis ===")
print(sentiment_result)

print("\n=== Text Classification ===")
print(text_classification_result)

=== Sentiment Analysis ===
[{'label': 'POSITIVE', 'score': 0.9998}]

=== Text Classification ===
[{'label': 'POSITIVE', 'score': 0.9998}]

