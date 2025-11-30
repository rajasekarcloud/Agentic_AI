from transformers import pipeline

# Example news headlines
news_articles = [
    "NASA announces new mission to explore Mars",
    "Stock markets rise as tech companies report strong earnings",
    "Local football team wins championship"
]

# Text Classification Pipeline
# Using a multi-class model for news categorization
classifier = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli"  # MNLI model works well for zero-shot classification
)

# Define candidate labels (categories)
labels = ["science", "finance", "sports", "politics", "technology"]

# Classify each article
for article in news_articles:
    result = classifier(article, candidate_labels=labels)
    print(f"Article: {article}")
    print(f"Predicted Category: {result['labels'][0]} (Score: {result['scores'][0]:.4f})")
    print("-" * 50)
