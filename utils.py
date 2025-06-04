# Note 1: Import library yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt

# Note 2: Load data dari file CSV
df = pd.read_csv('jml_kejadian_bunuh_diri__des_kel.csv')



# Note 3: Mencari kabupaten/kota dengan jumlah kasus terbanyak
top_kab = df.groupby('bps_nama_kabupaten_kota')['jumlah_kejadian'].sum().sort_values(ascending=False)
top_kab_csv = top_kab.head(1).reset_index()
top_kab_csv.to_csv('kabupaten_terbanyak.csv', index=False)

# Note 4: Mencari kabupaten/kota dengan jumlah kasus terendah
low_kab = top_kab[top_kab == top_kab.min()]
low_kab_csv = low_kab.reset_index()
low_kab_csv.to_csv('kabupaten_terendah.csv', index=False)

# Note 5: Visualisasi data dalam bentuk bar chart
plt.figure(figsize=(10,6))
top_kab.plot(kind='bar')
plt.title('Jumlah Kasus Bunuh Diri per Kabupaten/Kota')
plt.ylabel('Jumlah Kasus')
plt.tight_layout()
plt.savefig('bar_kabupaten.png')
plt.close()

# Note 6: Visualisasi data dalam bentuk pie chart
plt.figure(figsize=(8,8))
top_kab.plot(kind='pie', autopct='%1.1f%%')
plt.title('Persentase Kasus Bunuh Diri per Kabupaten/Kota')
plt.ylabel('')
plt.tight_layout()
plt.savefig('pie_kabupaten.png')
plt.close()


# Note 7: Analisis persentase kasus bunuh diri per kabupaten/kota
total = top_kab.sum()
persen = (top_kab / total * 100).reset_index()
persen.columns = ['Kabupaten/Kota', 'Persentase']
persen['Persentase'] = persen['Persentase'].apply(lambda x: round(x, 2))  # Membulatkan persentase ke 2 angka di belakang koma
persen.to_csv('persentase_kasus_kabupaten.csv', index=False)

# Note 8: Analisis tren jumlah kasus bunuh diri per tahun
if 'tahun' in df.columns:
    tren = df.groupby('tahun')['jumlah_kejadian'].sum()
    tren.to_csv('tren_kasus_per_tahun.csv')
    plt.figure(figsize=(8,5))
    tren.plot(marker='o')
    plt.title('Tren Jumlah Kasus Bunuh Diri per Tahun')
    plt.ylabel('Jumlah Kasus')
    plt.xlabel('Tahun')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tren_kasus_per_tahun.png')
    plt.close()
else:
    print("Kolom 'tahun' tidak ditemukan di DataFrame. Berikut adalah daftar kolom yang tersedia:")
    print(df.columns)

# Note 9: Analisis kasus bunuh diri per kecamatan
if 'bps_nama_kecamatan' in df.columns:
    kec = df.groupby('bps_nama_kecamatan')['jumlah_kejadian'].sum().sort_values(ascending=False)
    kec.to_csv('kasus_per_kecamatan.csv')
    plt.figure(figsize=(12,6))
    kec.plot(kind='bar')
    plt.title('Jumlah Kasus Bunuh Diri per Kecamatan')
    plt.ylabel('Jumlah Kasus')
    plt.tight_layout()
    plt.savefig('bar_kecamatan.png')
    plt.close()
else:
    print("Kolom 'bps_nama_kecamatan' tidak ditemukan di DataFrame. Berikut adalah daftar kolom yang tersedia:")
    print(df.columns)

# Note 10: Analisis kasus nol (kabupaten/kota dan kecamatan tanpa kasus)
all_kab = set(df['bps_nama_kabupaten_kota'].unique())
kab_ada_kasus = set(df[df['jumlah_kejadian'] > 0]['bps_nama_kabupaten_kota'].unique())
kab_no_case = all_kab - kab_ada_kasus
pd.DataFrame({'Kabupaten/Kota': list(kab_no_case)}).to_csv('kabupaten_tanpa_kasus.csv', index=False)

all_kec = set(df['bps_nama_kecamatan'].unique())
kec_ada_kasus = set(df[df['jumlah_kejadian'] > 0]['bps_nama_kecamatan'].unique())
kec_no_case = all_kec - kec_ada_kasus
pd.DataFrame({'Kecamatan': list(kec_no_case)}).to_csv('kecamatan_tanpa_kasus.csv', index=False)

# Note 11: Perbandingan jumlah kasus bunuh diri antara dua tahun tertentu
tahun1 = 2019
tahun2 = 2020
kasus1 = df[df['tahun'] == tahun1]['jumlah_kejadian'].sum()
kasus2 = df[df['tahun'] == tahun2]['jumlah_kejadian'].sum()
with open(f'perbandingan_{tahun1}_{tahun2}.txt', 'w') as f:
    f.write(f"Jumlah kasus tahun {tahun1}: {kasus1}\n")
    f.write(f"Jumlah kasus tahun {tahun2}: {kasus2}\n")
    if kasus1 > kasus2:
        f.write(f"Tahun {tahun1} lebih tinggi {kasus1 - kasus2} kasus.\n")
    elif kasus2 > kasus1:
        f.write(f"Tahun {tahun2} lebih tinggi {kasus2 - kasus1} kasus.\n")
    else:
        f.write("Jumlah kasus sama.\n")

# Note 12: Statistik deskriptif untuk kasus bunuh diri per kabupaten/kota dan kecamatan
stat_kab = top_kab.describe()[['mean', '50%', 'std']]
with open('statistik_kabupaten.txt', 'w') as f:
    f.write("Statistik Kasus per Kabupaten/Kota\n\n")
    f.write(stat_kab.to_string(float_format="%.2f"))
    f.write("\n\nCatatan:\n- mean: Rata-rata kasus\n- 50%: Median kasus\n- std: Standar deviasi")

stat_kec = kec.describe()[['mean', '50%', 'std']]
with open('statistik_kecamatan.txt', 'w') as f:
    f.write("Statistik Kasus per Kecamatan\n\n")
    f.write(stat_kec.to_string(float_format="%.2f"))
    f.write("\n\nCatatan:\n- mean: Rata-rata kasus\n- 50%: Median kasus\n- std: Standar deviasi")

# Note 13: Mencari 5 kecamatan dan desa dengan jumlah kasus bunuh diri terbanyak
top5_kec = kec.head(5).reset_index()
top5_kec.to_csv('top5_kecamatan.csv', index=False)

top_desa = df.groupby('bps_nama_desa_kelurahan')['jumlah_kejadian'].sum().sort_values(ascending=False)
top5_desa = top_desa.head(5).reset_index()
top5_desa.to_csv('top5_desa.csv', index=False)