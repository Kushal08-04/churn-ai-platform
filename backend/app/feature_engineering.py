import numpy as np

def transform_batch(df):
    # Example encoding
    df = df.copy()

    df["contract_type"] = df["contract_type"].map({
        "Monthly": 0,
        "Yearly": 1
    })

    return df[["tenure", "monthly_revenue", "support_calls", "contract_type"]]

def transform(data):
    engagement_ratio = data.logins_30d / 30
    ticket_risk = data.unresolved_tickets / (data.tickets_30d + 1)

    return np.array([
        data.logins_30d,
        data.feature_usage_drop,
        data.tickets_30d,
        data.unresolved_tickets,
        data.payment_failures,
        engagement_ratio,
        ticket_risk
    ]).reshape(1, -1)