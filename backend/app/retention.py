def generate_rule_based_strategy(df, summary):

    high_risk_df = df[df["risk_segment"] == "High"]

    if summary["total_revenue_at_risk"] > 100000:
        return (
            "Critical revenue exposure detected. "
            "Immediately assign dedicated account managers to top revenue customers. "
            "Offer annual plan discounts and proactive outreach."
        )

    if summary["high_risk_count"] > summary["medium_risk_count"]:
        return (
            "High churn concentration detected. "
            "Improve onboarding experience and reduce support response time."
        )

    if high_risk_df["contract_type"].mean() < 0.5:
        return (
            "Monthly subscribers are at higher risk. "
            "Introduce long-term contract incentives to improve retention."
        )

    return (
        "Customer base stable. Continue monitoring churn indicators monthly."
    )