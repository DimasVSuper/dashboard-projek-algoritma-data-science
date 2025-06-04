import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function LineChartTren({ data }) {
  if (!data || !data.tahunTerdata) return null;
  const trenData = data.tahunTerdata.map((tahun, idx) => ({
    tahun,
    total: data.trenKasus ? data.trenKasus[idx] : 0,
  }));

  return (
    <div>
      <h4>Tren Total Kasus Bunuh Diri per Tahun</h4>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={trenData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="tahun" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="total" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

