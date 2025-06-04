from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from API.models.dashboard_model import DashboardData, TopItem, Statistik
from API.database.mySql import SessionLocal
import pandas as pd

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard", response_model=DashboardData)
def get_dashboard(
    tahun: int = Query(None, description="Filter tahun (opsional)"),
    limit_top: int = Query(5, description="Jumlah top N terbanyak"),
    limit_bottom: int = Query(5, description="Jumlah bottom N terendah"),
    db: Session = Depends(get_db)
):
    # Ambil data dari MySQL
    query = """
        SELECT 
            kbd.tahun,
            kab.bps_nama_kabupaten_kota,
            kec.bps_nama_kecamatan,
            desa.bps_nama_desa_kelurahan,
            kbd.jumlah_kejadian
        FROM kejadian_bunuh_diri kbd
        JOIN desa_kelurahan desa ON kbd.bps_kode_desa_kelurahan = desa.bps_kode_desa_kelurahan
        JOIN kecamatan kec ON desa.bps_kode_kecamatan = kec.bps_kode_kecamatan
        JOIN kabupaten_kota kab ON kec.bps_kode_kabupaten_kota = kab.bps_kode_kabupaten_kota
    """
    df = pd.read_sql(query, db.bind)

    # Filter tahun jika dipilih
    if tahun is not None:
        df = df[df['tahun'] == tahun]

    # Ringkasan total kasus & tahun terdata
    totalKasus = int(df['jumlah_kejadian'].sum()) if not df.empty else 0
    tahunTerdata = sorted(df['tahun'].unique().tolist()) if not df.empty else []

    # Analisis kabupaten/kota
    top_kab = df.groupby('bps_nama_kabupaten_kota')['jumlah_kejadian'].sum().sort_values(ascending=False) if not df.empty else pd.Series(dtype=int)
    kabTerbanyak = [TopItem(nama=row[0], jumlah=int(row[1])) for row in top_kab.head(limit_top).items()]
    kabTerendah = [TopItem(nama=row[0], jumlah=int(row[1])) for row in top_kab.tail(limit_bottom).items()]

    # Analisis kecamatan
    top_kec = df.groupby('bps_nama_kecamatan')['jumlah_kejadian'].sum().sort_values(ascending=False) if not df.empty else pd.Series(dtype=int)
    top5Kec = [TopItem(nama=row[0], jumlah=int(row[1])) for row in top_kec.head(limit_top).items()]

    # Analisis desa
    top_desa = df.groupby('bps_nama_desa_kelurahan')['jumlah_kejadian'].sum().sort_values(ascending=False) if not df.empty else pd.Series(dtype=int)
    top5Desa = [TopItem(nama=row[0], jumlah=int(row[1])) for row in top_desa.head(limit_top).items()]

    # Kabupaten/kota tanpa kasus
    all_kab = set(df['bps_nama_kabupaten_kota'].unique()) if not df.empty else set()
    kab_ada_kasus = set(df[df['jumlah_kejadian'] > 0]['bps_nama_kabupaten_kota'].unique()) if not df.empty else set()
    kabTanpaKasus = sorted(list(all_kab - kab_ada_kasus))

    # Kecamatan tanpa kasus
    all_kec = set(df['bps_nama_kecamatan'].unique()) if not df.empty else set()
    kec_ada_kasus = set(df[df['jumlah_kejadian'] > 0]['bps_nama_kecamatan'].unique()) if not df.empty else set()
    kecTanpaKasus = sorted(list(all_kec - kec_ada_kasus))

    # Statistik deskriptif kabupaten/kota
    stat_kab = top_kab.describe() if not top_kab.empty else {"mean": 0, "50%": 0, "std": 0}
    statKab = Statistik(
        mean=round(float(stat_kab['mean']), 2) if 'mean' in stat_kab else 0,
        median=round(float(stat_kab['50%']), 2) if '50%' in stat_kab else 0,
        std=round(float(stat_kab['std']), 2) if 'std' in stat_kab else 0
    )

    # Statistik deskriptif kecamatan
    stat_kec = top_kec.describe() if not top_kec.empty else {"mean": 0, "50%": 0, "std": 0}
    statKec = Statistik(
        mean=round(float(stat_kec['mean']), 2) if 'mean' in stat_kec else 0,
        median=round(float(stat_kec['50%']), 2) if '50%' in stat_kec else 0,
        std=round(float(stat_kec['std']), 2) if 'std' in stat_kec else 0
    )

    # Highlight satuan terbanyak/terendah (ambil dari list top/bottom)
    kabTerbanyakItem = kabTerbanyak[0] if kabTerbanyak else TopItem(nama="", jumlah=0)
    kabTerendahItem = kabTerendah[0] if kabTerendah else TopItem(nama="", jumlah=0)
    kecTerbanyak = top5Kec[0] if top5Kec else TopItem(nama="", jumlah=0)
    desaTerbanyak = top5Desa[0] if top5Desa else TopItem(nama="", jumlah=0)

    # Data tren kasus per tahun (untuk line chart)
    trenKasus = []
    if not df.empty and tahun is None:
        tren = df.groupby('tahun')['jumlah_kejadian'].sum()
        trenKasus = [int(tren.get(t, 0)) for t in tahunTerdata]
    elif not df.empty and tahun is not None:
        # Jika filter tahun, trenKasus hanya 1 data
        trenKasus = [int(df['jumlah_kejadian'].sum())]

    return DashboardData(
        totalKasus=totalKasus,
        tahunTerdata=tahunTerdata,
        kabTerbanyak=kabTerbanyakItem,
        kabTerendah=kabTerendahItem,
        kecTerbanyak=kecTerbanyak,
        desaTerbanyak=desaTerbanyak,
        kabTanpaKasus=kabTanpaKasus,
        kecTanpaKasus=kecTanpaKasus,
        statKab=statKab,
        statKec=statKec,
        top5Kec=top5Kec,
        top5Desa=top5Desa,
        trenKasus=trenKasus  # <-- tambahkan ini
    )