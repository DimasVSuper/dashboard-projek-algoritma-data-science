SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS kejadian_bunuh_diri;
DROP TABLE IF EXISTS tahun;
DROP TABLE IF EXISTS satuan;
DROP TABLE IF EXISTS kemendagri_desa_kelurahan;
DROP TABLE IF EXISTS kemendagri_kecamatan;
DROP TABLE IF EXISTS desa_kelurahan;
DROP TABLE IF EXISTS kecamatan;
DROP TABLE IF EXISTS kabupaten_kota;
DROP TABLE IF EXISTS provinsi;
SET FOREIGN_KEY_CHECKS=1;
-- Select Playground
SELECT * FROM kejadian_bunuh_diri WHERE jumlah_kejadian >= 900;


-- Select (QUERY DENGAN BIJAK! Menggunakan RAM yang banyak)
-- 1. Hapus temporary table jika ada
DROP TEMPORARY TABLE IF EXISTS temp_kbd;

-- 2. Buat temporary table dari tabel utama (misal filter tahun 2019)
CREATE TEMPORARY TABLE temp_kbd AS
SELECT *
FROM kejadian_bunuh_diri
WHERE tahun = 2019
LIMIT 1; -- atau filter lain sesuai kebutuhan

-- 3. JOIN temp_kbd ke tabel referensi
SELECT 
    temp_kbd.id,
    temp_kbd.jumlah_kejadian,
    temp_kbd.satuan,
    temp_kbd.tahun,
    provinsi.nama_provinsi,
    kabupaten_kota.bps_nama_kabupaten_kota,
    kecamatan.bps_nama_kecamatan,
    desa_kelurahan.bps_nama_desa_kelurahan,
    kemendagri_kecamatan.kemendagri_nama_kecamatan,
    kemendagri_desa_kelurahan.kemendagri_nama_desa_kelurahan
FROM temp_kbd
JOIN desa_kelurahan 
    ON temp_kbd.bps_kode_desa_kelurahan = desa_kelurahan.bps_kode_desa_kelurahan
JOIN kecamatan 
    ON desa_kelurahan.bps_kode_kecamatan = kecamatan.bps_kode_kecamatan
JOIN kabupaten_kota 
    ON kecamatan.bps_kode_kabupaten_kota = kabupaten_kota.bps_kode_kabupaten_kota
JOIN provinsi 
    ON kabupaten_kota.kode_provinsi = provinsi.kode_provinsi
JOIN kemendagri_desa_kelurahan 
    ON temp_kbd.kemendagri_kode_desa_kelurahan = kemendagri_desa_kelurahan.kemendagri_kode_desa_kelurahan
JOIN kemendagri_kecamatan 
    ON kemendagri_desa_kelurahan.kemendagri_kode_kecamatan = kemendagri_kecamatan.kemendagri_kode_kecamatan
ORDER BY temp_kbd.id
LIMIT 1;



CREATE TABLE provinsi (
    kode_provinsi CHAR(2) PRIMARY KEY,
    nama_provinsi VARCHAR(100) NOT NULL
);

CREATE TABLE kabupaten_kota (
    bps_kode_kabupaten_kota CHAR(4) PRIMARY KEY,
    bps_nama_kabupaten_kota VARCHAR(100) NOT NULL,
    kode_provinsi CHAR(2) NOT NULL,
    FOREIGN KEY (kode_provinsi) REFERENCES provinsi(kode_provinsi)
);

CREATE TABLE kecamatan (
    bps_kode_kecamatan CHAR(7) PRIMARY KEY,
    bps_nama_kecamatan VARCHAR(100) NOT NULL,
    bps_kode_kabupaten_kota CHAR(4) NOT NULL,
    FOREIGN KEY (bps_kode_kabupaten_kota) REFERENCES kabupaten_kota(bps_kode_kabupaten_kota)
);

CREATE TABLE desa_kelurahan (
    bps_kode_desa_kelurahan CHAR(10) PRIMARY KEY,
    bps_nama_desa_kelurahan VARCHAR(100) NOT NULL,
    bps_kode_kecamatan CHAR(7) NOT NULL,
    FOREIGN KEY (bps_kode_kecamatan) REFERENCES kecamatan(bps_kode_kecamatan)
);

CREATE TABLE kemendagri_kecamatan (
    kemendagri_kode_kecamatan VARCHAR(20) PRIMARY KEY,
    kemendagri_nama_kecamatan VARCHAR(100) NOT NULL
);

CREATE TABLE kemendagri_desa_kelurahan (
    kemendagri_kode_desa_kelurahan VARCHAR(20) PRIMARY KEY,
    kemendagri_nama_desa_kelurahan VARCHAR(100) NOT NULL,
    kemendagri_kode_kecamatan VARCHAR(20) NOT NULL,
    FOREIGN KEY (kemendagri_kode_kecamatan) REFERENCES kemendagri_kecamatan(kemendagri_kode_kecamatan)
);

CREATE TABLE satuan (
    satuan VARCHAR(20) PRIMARY KEY
);

CREATE TABLE tahun (
    tahun YEAR PRIMARY KEY
);

CREATE TABLE kejadian_bunuh_diri (
    id INT PRIMARY KEY,
    bps_kode_desa_kelurahan CHAR(10) NOT NULL,
    kemendagri_kode_desa_kelurahan VARCHAR(20) NOT NULL,
    jumlah_kejadian INT NOT NULL,
    satuan VARCHAR(20) NOT NULL,
    tahun YEAR NOT NULL,
    FOREIGN KEY (bps_kode_desa_kelurahan) REFERENCES desa_kelurahan(bps_kode_desa_kelurahan),
    FOREIGN KEY (kemendagri_kode_desa_kelurahan) REFERENCES kemendagri_desa_kelurahan(kemendagri_kode_desa_kelurahan),
    FOREIGN KEY (satuan) REFERENCES satuan(satuan),
    FOREIGN KEY (tahun) REFERENCES tahun(tahun)
);
