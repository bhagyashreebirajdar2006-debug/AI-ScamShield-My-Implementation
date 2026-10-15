
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="AI ScamShield Message Detection")

# Load the new three-category model
model = joblib.load("scam_message_model_v2.joblib")


class MessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "ScamShield Message Detection API is running"}


@app.post("/check-message")
def check_message(request: MessageRequest):
    message = request.message.strip()

    if not message:
        return {"error": "Please enter a message."}

    probabilities = model.predict_proba([message])[0]
    classes = model.classes_

    scores = {
        label: round(float(probability) * 100, 2)
        for label, probability in zip(classes, probabilities)
    }

    category = max(scores, key=scores.get)

    return {
        "category": category.capitalize(),
        "confidence": scores[category],
        "scores": scores,
        "note": "Prototype prediction, not a guarantee."
    }
