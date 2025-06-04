# Dashboard Kasus Bunuh Diri Jawa Barat

Proyek ini adalah dashboard interaktif berbasis React dan FastAPI untuk visualisasi data kasus bunuh diri di Provinsi Jawa Barat. Data diambil dari database MySQL dan divisualisasikan dalam bentuk tabel, grafik batang, pie chart, dan line chart.

## Fitur

- **Filter tahun**: Lihat data seluruh tahun atau per tahun tertentu.
- **Limit Top/Bottom**: Atur jumlah kecamatan/desa dengan kasus terbanyak yang ingin ditampilkan.
- **Visualisasi**: 
  - Grafik batang (Top Kecamatan)
  - Pie chart (Proporsi Top Desa/Kelurahan)
  - Line chart (Tren kasus per tahun)
- **Statistik deskriptif**: Rata-rata, median, dan standar deviasi kasus per kabupaten/kota dan kecamatan.
- **Daftar wilayah tanpa kasus**: Kabupaten/kota dan kecamatan tanpa kasus bunuh diri.

## Struktur Folder

```
projek/
├── API/                   # Backend FastAPI
│   ├── controllers/
│   ├── models/
│   └── router/
├── src/                   # Frontend React
│   ├── components/
│   ├── pages/
│   └── styles/
├── jml_kejadian_bunuh_diri__des_kel.csv
├── bunuh_diri_jabar_2019.sql
├── package.json
├── vite.config.js
└── readme.md
```

## Instalasi Library

### Frontend (npm)

- Install semua dependency dasar:
  ```
  npm install
  ```
- Install library visualisasi:
  ```
  npm install recharts
  ```
- (Opsional, jika digunakan)  
  ```
  npm install axios react-router-dom
  ```

### Backend (pip)

- Install semua dependency dasar:
  ```
  pip install fastapi uvicorn sqlalchemy pandas pymysql
  ```
- Atau, jika ada file requirements:
  ```
  pip install -r requirements.txt
  ```

## Cara Menjalankan

### 1. **Backend (FastAPI + MySQL)**

- Pastikan MySQL sudah berjalan dan database sudah terisi data.
- Install dependencies Python:
  ```
  pip install -r requirements.txt
  ```
- Jalankan FastAPI:
  ```
  uvicorn API.main:app --reload
  ```

### 2. **Frontend (React + Vite)**

- Install dependencies:
  ```
  npm install
  ```
- Jalankan frontend:
  ```
  npm run dev
  ```
- Buka browser ke [http://localhost:5173](http://localhost:5173)

---

## Konfigurasi Penting

- ⚡ **Proxy Vite**: Sudah diatur di `vite.config.js` agar request `/api` diteruskan ke backend FastAPI (`http://127.0.0.1:8000`).
- 🌐 **CORS**: Sudah diaktifkan di backend agar frontend bisa fetch data dari API.

## Catatan Data

- 📊 Data utama diambil dari tabel MySQL, bisa di-import dari file `bunuh_diri_jabar_2019.sql`.
- 📝 Jika ingin update data, bisa gunakan script Python (`inputDataCsv.py`) untuk import dari CSV.

## Pengembangan & Testing

- 🔥 **Hot reload** aktif di frontend dan backend (gunakan `--reload` di uvicorn dan `npm run dev` di Vite).
- 🧪 Untuk pengujian, pastikan backend dan frontend berjalan bersamaan.

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan tugas kuliah. Silakan gunakan dan modifikasi sesuai kebutuhan.

---

**Kontributor:**  
- 🙋‍♂️ Dimas  
- 🤖 Github Copilot  
- 🤖 OpenAI ChatGPT

---

❓ Jika ada pertanyaan atau ingin kontribusi, silakan buat issue atau pull request di repository ini.