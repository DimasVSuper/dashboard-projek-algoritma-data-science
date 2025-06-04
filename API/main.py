from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.router.router import router

app = FastAPI()

# Aktifkan CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ganti sesuai alamat frontend kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)