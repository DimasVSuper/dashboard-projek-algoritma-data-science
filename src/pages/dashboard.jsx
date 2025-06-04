import React, { useEffect, useState } from "react";
import BarChartKasus from "../components/BarChartKasus";
import PieChartKasus from "../components/PieChartKasus";
import LineChartTren from "../components/LineChartTren";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [tahun, setTahun] = useState("");
  const [limit, setLimit] = useState(5);
  const [data, setData] = useState(null);
  const [showVis, setShowVis] = useState(false);

  // Fetch data dashboard dari API
  const fetchDashboard = () => {
    let url = `/api/dashboard?limit_top=${limit}&limit_bottom=${limit}`;
    if (tahun) url += `&tahun=${tahun}`;
    fetch(url)
      .then((res) => res.json())
      .then(setData);
  };

  // Fetch otomatis hanya jika tahun kosong
  useEffect(() => {
    if (!tahun) {
      fetchDashboard();
    }
    // eslint-disable-next-line
  }, [limit, tahun]);

  // Handler tombol tampilkan (hanya fetch jika tahun diisi)
  const handleTampilkan = () => {
    if (tahun) {
      fetchDashboard();
    }
  };

  return (
    <div>
      <h1>Dashboard Kasus Bunuh Diri Jawa Barat</h1>
      <p>Selamat datang di dashboard data kasus bunuh diri Jabar.</p>

      <div style={{ marginBottom: 16 }}>
        <label>
          Pilih Tahun:{" "}
          <input
            type="number"
            value={tahun}
            onChange={(e) => setTahun(e.target.value)}
            placeholder="Contoh: 2019"
          />
        </label>
        <label style={{ marginLeft: 16 }}>
          Limit Top/Bottom:{" "}
          <input
            type="number"
            value={limit}
            min={1}
            onChange={(e) => setLimit(e.target.value)}
          />
        </label>
        <button
          style={{ marginLeft: 16 }}
          onClick={handleTampilkan}
          disabled={!tahun}
        >
          Tampilkan
        </button>
      </div>

      {!data ? (
        <p>Memuat data...</p>
      ) : (
        <>
          <h2>Ringkasan Data</h2>
          <ul>
            <li>
              Total kasus: <b>{data.totalKasus}</b>
            </li>
            <li>
              Tahun terdata: <b>{data.tahunTerdata.join(", ")}</b>
            </li>
            <li>
              Kabupaten/kota dengan kasus terbanyak:{" "}
              <b>
                {data.kabTerbanyak.nama} ({data.kabTerbanyak.jumlah} kasus)
              </b>
            </li>
            <li>
              Kabupaten/kota dengan kasus terendah:{" "}
              <b>
                {data.kabTerendah.nama} ({data.kabTerendah.jumlah} kasus)
              </b>
            </li>
            <li>
              Kecamatan dengan kasus terbanyak:{" "}
              <b>
                {data.kecTerbanyak.nama} ({data.kecTerbanyak.jumlah} kasus)
              </b>
            </li>
            <li>
              Desa/kelurahan dengan kasus terbanyak:{" "}
              <b>
                {data.desaTerbanyak.nama} ({data.desaTerbanyak.jumlah} kasus)
              </b>
            </li>
          </ul>

          <h2>Kabupaten/Kota Tanpa Kasus</h2>
          <ul>
            {data.kabTanpaKasus.map((kab, idx) => (
              <li key={idx}>{kab}</li>
            ))}
          </ul>

          <h2>Kecamatan Tanpa Kasus</h2>
          <ul>
            {data.kecTanpaKasus.map((kec, idx) => (
              <li key={idx}>{kec}</li>
            ))}
          </ul>

          <h2>Statistik Deskriptif Kabupaten/Kota</h2>
          <ul>
            <li>Rata-rata: {data.statKab.mean}</li>
            <li>Median: {data.statKab.median}</li>
            <li>Standar deviasi: {data.statKab.std}</li>
          </ul>

          <h2>Statistik Deskriptif Kecamatan</h2>
          <ul>
            <li>Rata-rata: {data.statKec.mean}</li>
            <li>Median: {data.statKec.median}</li>
            <li>Standar deviasi: {data.statKec.std}</li>
          </ul>

          <h2>Top {limit} Kecamatan dengan Kasus Terbanyak</h2>
          <ol>
            {data.top5Kec.map((kec, idx) => (
              <li key={idx}>
                {kec.nama} ({kec.jumlah} kasus)
              </li>
            ))}
          </ol>

          <h2>Top {limit} Desa/Kelurahan dengan Kasus Terbanyak</h2>
          <ol>
            {data.top5Desa.map((desa, idx) => (
              <li key={idx}>
                {desa.nama} ({desa.jumlah} kasus)
              </li>
            ))}
          </ol>

          <button
            style={{ margin: "24px 0", padding: "8px 16px" }}
            onClick={() => setShowVis((v) => !v)}
          >
            {showVis ? "Sembunyikan Visualisasi" : "Tampilkan Visualisasi?"}
          </button>

          {showVis && (
            <div>
              <BarChartKasus data={data} />
              <PieChartKasus data={data} />
              <LineChartTren data={data} />
            </div>
          )}
        </>
      )}
    </div>
  );
}