
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load the SMS dataset
data = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)

# Clean duplicate and missing messages
data = data.dropna()
data = data.drop_duplicates(subset="message")

# Map the original dataset labels
data["label"] = data["label"].map({
    "ham": "safe",
    "spam": "scam"
})

data = data.dropna(subset=["label"])

X = data["message"]
y = data["label"]

# Keep some messages aside for testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create and train our model
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        strip_accents="unicode"
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ))
])

model.fit(X_train, y_train)

# Evaluate on messages not used for training
predictions = model.predict(X_test)

print("\n--- MODEL EVALUATION ---")
print("Training messages:", len(X_train))
print("Test messages:", len(X_test))
print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save the trained model
joblib.dump(model, "scam_message_model.joblib")

print("\nModel saved successfully!")
