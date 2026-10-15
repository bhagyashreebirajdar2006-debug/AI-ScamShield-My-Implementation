
import joblib

# Load our trained model
model = joblib.load("scam_message_model.joblib")

print("AI ScamShield - Message Detection")
print("Type 'exit' to stop.\n")

while True:
    message = input("Enter a message: ").strip()

    if message.lower() == "exit":
        print("Testing finished.")
        break

    if not message:
        print("Please enter a message.\n")
        continue

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]
    confidence = max(probabilities) * 100

    if prediction == "scam":
        print("Result: Potential spam/scam")
    else:
        print("Result: Likely legitimate")

    print(f"Model confidence: {confidence:.1f}%")
    print("Note: This is a prediction, not a guarantee.\n")
