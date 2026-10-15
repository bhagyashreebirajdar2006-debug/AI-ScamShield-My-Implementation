
import pandas as pd
import joblib

# Load the trained ScamShield model
model = joblib.load("scam_message_model.joblib")

# Read the test messages from the CSV file
tests = pd.read_csv("indian_test_messages.csv")

correct = 0

print("\nAI ScamShield - Message Evaluation\n")

for _, row in tests.iterrows():
    message = row["message"]
    expected = row["label"].strip().lower()

    predicted = model.predict([message])[0]

    if predicted == expected:
        status = "PASS"
        correct += 1
    else:
        status = "CHECK"

    print("Message:", message)
    print("Expected:", expected)
    print("Predicted:", predicted)
    print("Status:", status)
    print("-" * 45)

print(f"\nMatching examples: {correct}/{len(tests)}")
print("These are preliminary tests, not verified real-world accuracy.")
