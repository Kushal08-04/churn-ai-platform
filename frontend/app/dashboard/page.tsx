"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: any) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (!file.name.endsWith(".csv")) {
      setError("Please upload a valid CSV file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/upload-csv", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Upload failed");
      }

      const data = await response.json();
      setAnalytics(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-10">
      <h1 className="text-4xl font-bold mb-10">
        AI Churn Analytics Dashboard
      </h1>

      {/* FILE UPLOAD */}
      <div className="mb-8">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          className="bg-gray-800 p-3 rounded"
        />
      </div>

      {loading && (
        <div className="text-center text-gray-400 mb-6">
          Processing CSV...
        </div>
      )}

      {error && (
        <div className="text-red-500 mb-6">
          {error}
        </div>
      )}

      {!analytics && !loading && (
        <div className="text-gray-500">
          Upload a CSV file to see analytics.
        </div>
      )}

      {analytics && (
        <>
          {/* SUMMARY CARDS */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
            <Card title="High Risk" value={analytics.summary.high_risk_count} />
            <Card title="Medium Risk" value={analytics.summary.medium_risk_count} />
            <Card title="Low Risk" value={analytics.summary.low_risk_count} />
            <Card
              title="Revenue At Risk"
              value={`$${analytics.summary.total_revenue_at_risk.toFixed(2)}`}
            />
          </div>

          {/* CHARTS */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">

            {/* Risk Pie Chart */}
            <div className="bg-gray-900 p-6 rounded-2xl">
              <h2 className="mb-4 font-bold">Risk Distribution</h2>

              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "High", value: analytics.summary.high_risk_count },
                      { name: "Medium", value: analytics.summary.medium_risk_count },
                      { name: "Low", value: analytics.summary.low_risk_count }
                    ]}
                    dataKey="value"
                    outerRadius={100}
                  >
                    <Cell fill="#ff4d4d" />
                    <Cell fill="#ffa500" />
                    <Cell fill="#00cc66" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Revenue Trend Line Chart */}
            <div className="bg-gray-900 p-6 rounded-2xl">
              <h2 className="mb-4 font-bold">Revenue at Risk Trend</h2>

              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={analytics.revenue_trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="tenure" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="revenue_at_risk"
                    stroke="#8884d8"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

          </div>

          {/* RETENTION STRATEGY */}
          <div className="mt-10 bg-gray-900 p-6 rounded-2xl">
            <h2 className="text-xl font-bold mb-4">
              Retention Strategy
            </h2>
            <p className="text-gray-300 leading-relaxed">
              {analytics.retention_strategy}
            </p>
          </div>
        </>
      )}
    </div>
  );
}

function Card({ title, value }: any) {
  return (
    <div className="bg-gray-900 p-6 rounded-2xl">
      <h2 className="text-gray-400 text-sm">{title}</h2>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}