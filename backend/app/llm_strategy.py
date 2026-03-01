import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_llm_strategy(summary):

    prompt = f"""
    Churn Analytics Summary:

    Total Customers: {summary['total_customers']}
    High Risk: {summary['high_risk_count']}
    Medium Risk: {summary['medium_risk_count']}
    Revenue at Risk: {summary['total_revenue_at_risk']}

    Provide:
    1. Root cause analysis
    2. 3 retention strategies
    3. Executive summary
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content