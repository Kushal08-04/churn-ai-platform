import pandas as pd
import joblib
from xgboost import XGBClassifier

df = pd.read_csv("sample_data.csv")

X = df.drop("churn", axis=1)
y = df["churn"]

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1
)

model.fit(X, y)

joblib.dump(model, "model.joblib")

print("Model trained and saved successfully.")