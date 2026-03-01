from fastapi import FastAPI
from app.schemas import CustomerData
from app.feature_engineering import transform
from app.model import load_model
from app.explainability import explain

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = load_model()

@app.get("/")
def home():
    return {"message": "Churn AI Running"}

@app.post("/predict")
def predict(data: CustomerData):

    features = transform(data)
    probability = model.predict_proba(features)[0][1]

    revenue_at_risk = probability * data.monthly_revenue

    explanation = explain(model, features)

    return {
        "churn_probability": float(probability),
        "risk_segment":
            "High" if probability > 0.6 else
            "Medium" if probability > 0.3 else
            "Low",
        "revenue_at_risk": float(revenue_at_risk),
        "feature_impact": explanation
    }