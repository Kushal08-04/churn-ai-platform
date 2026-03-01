from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

from app.schemas import CustomerData
from app.feature_engineering import transform
from app.model import load_model

# =========================================================
# APP INITIALIZATION
# =========================================================

app = FastAPI(title="Churn AI Platform")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()

# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def health():
    return {"status": "Churn AI Backend Running"}

# =========================================================
# SINGLE CUSTOMER PREDICTION
# =========================================================

@app.post("/predict")
def predict(data: CustomerData):

    try:
        features = transform(data)
        probability = model.predict_proba(features)[0][1]

        revenue_at_risk = probability * data.monthly_revenue

        return {
            "churn_probability": float(probability),
            "risk_segment":
                "High" if probability > 0.6 else
                "Medium" if probability > 0.3 else
                "Low",
            "revenue_at_risk": float(revenue_at_risk),
            "feature_impact": {}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# BATCH CSV UPLOAD + ANALYTICS
# =========================================================

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    # -----------------------------------------------------
    # REQUIRED COLUMNS (MATCH MODEL TRAINING DATA)
    # -----------------------------------------------------

    required_columns = [
        "logins_30d",
        "feature_usage_drop",
        "tickets_30d",
        "unresolved_tickets",
        "payment_failures",
        "monthly_revenue"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required column: {col}"
            )

    records = []

    # -----------------------------------------------------
    # ROW-WISE PREDICTION USING SAME TRANSFORM PIPELINE
    # -----------------------------------------------------

    for _, row in df.iterrows():

        customer = CustomerData(
            logins_30d=row["logins_30d"],
            feature_usage_drop=row["feature_usage_drop"],
            tickets_30d=row["tickets_30d"],
            unresolved_tickets=row["unresolved_tickets"],
            payment_failures=row["payment_failures"],
            monthly_revenue=row["monthly_revenue"]
        )

        features = transform(customer)

        probability = model.predict_proba(features)[0][1]
        print("Probability:", probability)
        revenue_at_risk = probability * row["monthly_revenue"]

        record = row.to_dict()
        record["churn_probability"] = float(probability)
        record["revenue_at_risk"] = float(revenue_at_risk)
        record["risk_segment"] = (
            "High" if probability > 0.6
            else "Medium" if probability > 0.3
            else "Low"
        )

        records.append(record)

    result_df = pd.DataFrame(records)

    # =====================================================
    # ANALYTICS SUMMARY
    # =====================================================

    summary = {
        "high_risk_count": int((result_df["risk_segment"] == "High").sum()),
        "medium_risk_count": int((result_df["risk_segment"] == "Medium").sum()),
        "low_risk_count": int((result_df["risk_segment"] == "Low").sum()),
        "total_customers": int(len(result_df)),
        "total_revenue_at_risk": float(result_df["revenue_at_risk"].sum())
    }

    # =====================================================
    # REVENUE TREND (FOR LINE CHART)
    # =====================================================

    revenue_trend = (
        result_df.groupby("logins_30d")["revenue_at_risk"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    # =====================================================
    # RETENTION STRATEGY
    # =====================================================

    retention_strategy = generate_retention_strategy(summary)

    return {
        "summary": summary,
        "revenue_trend": revenue_trend,
        "records": result_df.to_dict(orient="records"),
        "retention_strategy": retention_strategy
    }

# =========================================================
# RETENTION STRATEGY ENGINE
# =========================================================

def generate_retention_strategy(summary):

    if summary["total_revenue_at_risk"] > 100000:
        return (
            "Critical revenue exposure detected. "
            "Deploy premium retention strategy including proactive account management, "
            "annual contract incentives, and targeted engagement campaigns."
        )

    if summary["high_risk_count"] > summary["medium_risk_count"]:
        return (
            "High churn concentration detected. "
            "Improve product engagement, reduce feature drop-off, "
            "resolve support tickets faster, and introduce loyalty rewards."
        )

    return (
        "Customer base appears stable. "
        "Maintain engagement initiatives and monitor churn indicators monthly."
    )