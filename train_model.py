import pandas as pd
import joblib
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Ensure you have necessary resources for text processing
nltk.download('stopwords')

# Sample Training Data (You can expand this with real expenses)
data = {
    "description": [
        "Bought vegetables and fruits", "Dinner at a restaurant",
        "Monthly gym subscription", "Paid for Netflix",
        "Taxi fare to office", "Flight ticket to Mumbai",
        "Bought a laptop", "Paid electricity bill"
    ],
    "category": [
        "Groceries", "Dining", "Fitness", "Entertainment",
        "Transport", "Travel", "Shopping", "Utilities"
    ]
}

df = pd.DataFrame(data)

# Create a text-processing & classification pipeline
model_pipeline = Pipeline([
    ("vectorizer", CountVectorizer(stop_words="english")),
    ("classifier", MultinomialNB())
])

# Train the model
model_pipeline.fit(df["description"], df["category"])

# Save the model
joblib.dump(model_pipeline, "expense_classifier.pkl")

print("Model trained and saved successfully!")
