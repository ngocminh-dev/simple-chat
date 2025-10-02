"""FastAPI"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .modules.chat.router import router as chat_router
from .modules.core.router import router as core_router
from .modules.user.router import router as user_router

app = FastAPI()

# Cấu hình CORS
origins = [
    "http://localhost:5173",  # frontend vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(core_router)
app.include_router(user_router)
app.include_router(chat_router)
