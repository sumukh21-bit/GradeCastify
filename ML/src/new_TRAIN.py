from MLP import *
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import sklearn.model_selection as model_selection
import sklearn.preprocessing as preprocessing
import joblib

from xgboost import XGBClassifier
import os


df = pd.read_csv("ML/data/studentperformancedata.csv")
df["Extracurricular_Activities"] = df["Extracurricular_Activities"].map({"Yes": 1, "No": 0})
feature_names = ["Attendance", "Midterm", "Assignments", "Quizzes", "Participation", "Projects", "Study Hours", "Extracurricular", "Stress", "Sleep"]

df = df.dropna() 

X = df[["Attendance (%)", "Midterm_Score","Assignments_Avg", "Quizzes_Avg", "Participation_Score", "Projects_Score", "Study_Hours_per_Week", "Extracurricular_Activities", "Stress_Level (1-10)","Sleep_Hours_per_Night"]].values
y = df["Grade"].map(grade_map).values


X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
    )

scaler = preprocessing.StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = XGBClassifier(
    n_estimators=50,
    max_depth=4,
    learning_rate=0.1,
    eval_metric="mlogloss"
)

model.fit(
    X_train, y_train
)
joblib.dump(model, "ML/artifacts/xgb_model.pkl")
joblib.dump(scaler, "ML/artifacts/scaler.pkl")

preds = model.predict(X_test)

print("Classification Report:")
print(metrics.classification_report(y_test, preds, target_names=list(grade_map.keys())))
print(f"Accuracy: {metrics.accuracy_score(y_test, preds):.2f}")


