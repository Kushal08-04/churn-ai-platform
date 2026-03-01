import numpy as np

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