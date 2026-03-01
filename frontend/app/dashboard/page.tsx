"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {

  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        logins_30d: 5,
        feature_usage_drop: 40,
        tickets_30d: 3,
        unresolved_tickets: 2,
        payment_failures: 1,
        monthly_revenue: 200
      })
    })
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-10">
      <h1 className="text-4xl font-bold mb-10">
        AI Churn Dashboard
      </h1>

      <div className="grid grid-cols-3 gap-6">

        <div className="bg-gray-900 p-6 rounded-2xl">
          <h2 className="text-gray-400 text-sm">Churn Probability</h2>
          <p className="text-3xl font-bold mt-2">
            {data.churn_probability.toFixed(2)}
          </p>
        </div>

        <div className="bg-gray-900 p-6 rounded-2xl">
          <h2 className="text-gray-400 text-sm">Risk Segment</h2>
          <p className="text-3xl font-bold mt-2">
            {data.risk_segment}
          </p>
        </div>

        <div className="bg-gray-900 p-6 rounded-2xl">
          <h2 className="text-gray-400 text-sm">Revenue At Risk</h2>
          <p className="text-3xl font-bold mt-2">
            ${data.revenue_at_risk.toFixed(2)}
          </p>
        </div>

      </div>
    </div>
  );
}