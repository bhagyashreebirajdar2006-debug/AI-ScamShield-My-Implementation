
import pandas as pd

data = pd.read_csv("scam_training_data.csv")

print("\n--- TRAINING DATA CHECK ---")
print("Total messages:", len(data))

print("\nMessages per category:")
print(data["label"].value_counts())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate messages:", data["message"].duplicated().sum())

print("\nLabels found:")
print(sorted(data["label"].dropna().unique()))

required_labels = {"safe", "suspicious", "scam"}

if set(data["label"].dropna().unique()) == required_labels:
    print("\nAll three categories are present.")
else:
    print("\nWarning: One or more categories are missing.")

print("\nDataset check complete.")
