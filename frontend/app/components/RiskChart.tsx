"use client";
import { PieChart, Pie, Cell, Tooltip } from "recharts";

export default function RiskChart({ data }: any) {

  const counts = [
    { name: "High", value: data.filter((d:any) => d.risk_segment === "High").length },
    { name: "Medium", value: data.filter((d:any) => d.risk_segment === "Medium").length },
    { name: "Low", value: data.filter((d:any) => d.risk_segment === "Low").length },
  ];

  return (
    <PieChart width={400} height={300}>
      <Pie data={counts} dataKey="value" nameKey="name" outerRadius={100}>
        {counts.map((_, index) => (
          <Cell key={index} />
        ))}
      </Pie>
      <Tooltip />
    </PieChart>
  );
}