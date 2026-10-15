# ScamShield Message Detection API

Prototype SMS scam classifier using TF-IDF and scikit-learn Logistic Regression.

## Setup
Run: `pip install -r requirements.txt`

## Run API
Run: `uvicorn app:app --host 0.0.0.0 --port 8000`

Endpoint: POST /check-message.

This is a prototype and may misclassify messages.
