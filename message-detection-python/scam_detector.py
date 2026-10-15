
import joblib

MODEL_PATH = "scam_message_model.joblib"

# Load the existing trained model
model = joblib.load(MODEL_PATH)


def detect_message(message):
    if not isinstance(message, str) or not message.strip():
        return {
            "category": "Suspicious",
            "confidence": 0.0,
            "message": "Please enter a valid text message."
        }

    probabilities = model.predict_proba([message])[0]
    classes = model.classes_

    probability_map = {
        label: float(probability)
        for label, probability in zip(classes, probabilities)
    }

    scam_probability = probability_map.get("scam", 0.0)
    safe_probability = probability_map.get("safe", 0.0)

    # Conservative initial thresholds; these require validation.
    if scam_probability >= 0.80:
        category = "Scam"
    elif scam_probability >= 0.40:
        category = "Suspicious"
    else:
        category = "Safe"

    confidence = max(scam_probability, safe_probability) * 100

    return {
        "category": category,
        "confidence": round(confidence, 2),
        "scam_probability": round(scam_probability * 100, 2),
        "message": "Prediction only; not a guarantee."
    }


if __name__ == "__main__":
    print("AI ScamShield - Scam Message Detection")
    print("Type 'exit' to stop.\n")

    while True:
        text = input("Enter SMS: ")

        if text.strip().lower() == "exit":
            break

        result = detect_message(text)
        print("Category:", result["category"])
        print("Model confidence:", result["confidence"], "%")
        print("Scam probability:", result["scam_probability"], "%")
        print(result["message"])
        print("-" * 40)
