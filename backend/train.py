import pandas as pd
import joblib
from xgboost import XGBClassifier

df = pd.read_csv("sample_data.csv")

X = df.drop("churn", axis=1)
y = df["churn"]

XGBClassifier(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    scale_pos_weight=2,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "model.joblib")

print("Model trained and saved successfully.")