from pydantic import BaseModel
from typing import List

class TopItem(BaseModel):
    nama: str
    jumlah: int

class Statistik(BaseModel):
    mean: float
    median: float
    std: float

class DashboardData(BaseModel):
    totalKasus: int
    tahunTerdata: List[int]
    kabTerbanyak: TopItem
    kabTerendah: TopItem
    kecTerbanyak: TopItem
    desaTerbanyak: TopItem
    kabTanpaKasus: List[str]
    kecTanpaKasus: List[str]
    statKab: Statistik
    statKec: Statistik
    top5Kec: List[TopItem]
    top5Desa: List[TopItem]
    trenKasus: List[int]  # <-- tambahkan field ini untuk tren kasus per tahun