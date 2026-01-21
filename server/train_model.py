import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "../fraudulent_jobs.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_FILE = os.path.join(MODEL_DIR, "basic_model.pkl")

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found at {DATA_FILE}")
        return None
    print("Loading data...")
    return pd.read_csv(DATA_FILE)

def preprocess_data(df):
    print("Preprocessing data...")
    # Fill missing values
    df.fillna(" ", inplace=True)
    
    # Combine text columns
    df['text'] = df['title'] + " " + df['company_profile'] + " " + \
                 df['description'] + " " + df['requirements'] + " " + df['benefits']
    
    return df['text'], df['fraudulent']

def train():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    df = load_data()
    if df is None:
        return

    X, y = preprocess_data(df)
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build Pipeline: Bag of Words -> Naive Bayes
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english', max_features=5000)),
        ('classifier', MultinomialNB())
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating model...")
    predictions = pipeline.predict(X_val)
    print(f"Accuracy: {accuracy_score(y_val, predictions)}")
    print(classification_report(y_val, predictions))
    
    # Save
    print(f"Saving model to {MODEL_FILE}...")
    joblib.dump(pipeline, MODEL_FILE)
    print("Done!")

if __name__ == "__main__":
    train()
