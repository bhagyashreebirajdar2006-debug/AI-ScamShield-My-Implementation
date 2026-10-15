
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

data = pd.read_csv("scam_training_data.csv")
data = data.dropna(subset=["label", "message"])
data["label"] = data["label"].str.strip().str.lower()
data["message"] = data["message"].astype(str).str.strip()
data = data[data["label"].isin(["safe", "suspicious", "scam"])]
data = data[data["message"] != ""]
data = data.drop_duplicates(subset=["message"])

print("Examples per category:")
print(data["label"].value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    data["message"], data["label"],
    test_size=0.25, random_state=42, stratify=data["label"]
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True, ngram_range=(1, 2),
        strip_accents="unicode"
    )),
    ("classifier", LogisticRegression(
        max_iter=1000, class_weight="balanced",
        random_state=42
    ))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("\nEvaluation report:")
print(classification_report(
    y_test, predictions, zero_division=0
))

joblib.dump(model, "scam_message_model_v2.joblib")
print("\nSaved as scam_message_model_v2.joblib")
