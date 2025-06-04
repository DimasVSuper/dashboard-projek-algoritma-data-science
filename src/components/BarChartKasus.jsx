import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function BarChartKasus({ data }) {
  if (!data || !data.top5Kec) return null;
  return (
    <div>
      <h4>Top Kecamatan dengan Kasus Terbanyak</h4>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data.top5Kec}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="nama" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="jumlah" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

