
import pandas as pd

# Load the original SMS dataset
data = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)

# Display dataset summary
print("\n--- DATASET SUMMARY ---")
print("Total messages:", len(data))

print("\n--- LABEL COUNTS ---")
print(data["label"].value_counts())

# Show 10 examples of spam messages
print("\n--- EXAMPLE SPAM MESSAGES ---")
spam_messages = data.loc[data["label"] == "spam", "message"].head(10)

for message in spam_messages:
    print("-", message)

# Show 10 examples of legitimate messages
print("\n--- EXAMPLE LEGITIMATE MESSAGES ---")
safe_messages = data.loc[data["label"] == "ham", "message"].head(10)

for message in safe_messages:
    print("-", message)

print("\n--- INSPECTION COMPLETE ---")
print("The dataset has not been modified.")
