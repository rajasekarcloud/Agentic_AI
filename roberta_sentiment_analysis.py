from transformers import pipeline

# Initialize the text classification pipeline with a RoBERTa model
classifier = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-sentiment')

# Array of example texts for classification
comments = [
    "This product is absolutely amazing. I highly recommend it to everyone!",  # Positive feedback
    "It's okay, but nothing special. I expected more for the price.",           # Neutral feedback
    "Terrible experience. The product broke within a week!",                   # Bad feedback
    "Good value for the money. I'm satisfied with this purchase."              # Positive feedback
]

# Loop through each comment in the array
for text in comments:
    # Get classification results
    result = classifier(text)
    
    # Translate labels to human-readable sentiments
    label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
    sentiment = label_map[result[0]['label']]
    
    # Display the classification result
    print(f"Text: {text}")
    print(f"Sentiment: {sentiment}, Confidence: {result[0]['score']:.2f}")
    print("-" * 50)
