import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import joblib
import os
import numpy as np

os.makedirs("ml", exist_ok=True)

df = pd.read_csv("ml_dataset.csv")

# label created
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

model = RandomForestClassifier(
    n_estimators=50,
    max_features=1,
    max_depth=3,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

model.fit(X_train, y_train)

# ACCURACY OF MODEL
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)

# ACCURACY GRAPH
plt.figure()
plt.bar(["Train Accuracy", "Test Accuracy"], [train_acc, test_acc])
plt.title("Model Accuracy Comparison")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("app/ml/accuracy_comparison.png")
plt.close()

# CONFUSION MATRIX 
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Confusion Matrix")
plt.savefig("app/ml/confusion_matrix.png")
plt.close()

# ACCURACY VS TREES GRAPH
trees = [10, 50, 100, 150]
scores = []

for n in trees:
    temp_model = RandomForestClassifier(n_estimators=n)
    temp_model.fit(X_train, y_train)
    scores.append(temp_model.score(X_test, y_test))

plt.figure()
plt.plot(trees, scores, marker='o')
plt.title("Accuracy vs Number of Trees")
plt.xlabel("Number of Trees")
plt.ylabel("Accuracy")
plt.savefig("app/ml/accuracy_vs_trees.png")
plt.close()

# SAVE MODEL
joblib.dump(model, "app/ml/weakness_model.pkl")

print("✅ Model and graphs saved in 'ml/' folder")
