import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

os.makedirs("ml", exist_ok=True)

df = pd.read_csv("ml_dataset.csv")

# create label
def difficulty_label(acc):
    if acc < 0.4:
        return "easy"
    elif acc < 0.7:
        return "medium"
    else:
        return "hard"

df["difficulty"] = df["accuracy"].apply(difficulty_label)

X = df[[
    "attempts",
    "avg_score",
    "avg_time"
]]

y = df["difficulty"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()

model.fit(X_train, y_train)

print("Model accuracy:", model.score(X_test, y_test))

joblib.dump(model, "ml/weakness_model.pkl")