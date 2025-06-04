import pandas as pd
from sqlalchemy import create_engine

user = 'root'
password = ''
host = 'localhost'
port = 3306
database = 'bunuh_diri_jabar_2019'

df = pd.read_csv('jml_kejadian_bunuh_diri__des_kel.csv')
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Input data referensi (tanpa duplikat)
df[['kode_provinsi', 'nama_provinsi']].drop_duplicates().to_sql('provinsi', engine, if_exists='append', index=False)
df[['bps_kode_kabupaten_kota', 'bps_nama_kabupaten_kota', 'kode_provinsi']].drop_duplicates().to_sql('kabupaten_kota', engine, if_exists='append', index=False)
df[['bps_kode_kecamatan', 'bps_nama_kecamatan', 'bps_kode_kabupaten_kota']].drop_duplicates().to_sql('kecamatan', engine, if_exists='append', index=False)
df[['bps_kode_desa_kelurahan', 'bps_nama_desa_kelurahan', 'bps_kode_kecamatan']].drop_duplicates().to_sql('desa_kelurahan', engine, if_exists='append', index=False)
df[['kemendagri_kode_kecamatan', 'kemendagri_nama_kecamatan']].drop_duplicates().to_sql('kemendagri_kecamatan', engine, if_exists='append', index=False)
df[['kemendagri_kode_desa_kelurahan', 'kemendagri_nama_desa_kelurahan', 'kemendagri_kode_kecamatan']].drop_duplicates().to_sql('kemendagri_desa_kelurahan', engine, if_exists='append', index=False)
df[['satuan']].drop_duplicates().to_sql('satuan', engine, if_exists='append', index=False)
df[['tahun']].drop_duplicates().to_sql('tahun', engine, if_exists='append', index=False)

# Input data utama
df[['id', 'bps_kode_desa_kelurahan', 'kemendagri_kode_desa_kelurahan', 'jumlah_kejadian', 'satuan', 'tahun']].to_sql('kejadian_bunuh_diri', engine, if_exists='append', index=False)

print("Import selesai!")
