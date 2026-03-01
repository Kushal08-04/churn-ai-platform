from pydantic import BaseModel

class CustomerData(BaseModel):
    logins_30d: int
    feature_usage_drop: float
    tickets_30d: int
    unresolved_tickets: int
    payment_failures: int
    monthly_revenue: float