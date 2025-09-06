from typing import Optional
from fastapi import FastAPI, HTTPException
import qrcode
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import UploadFile, File, Form
from PIL import Image, ImageDraw
import io
from .routers import qrcode

app = FastAPI(
            title="QRForge",
            description="A simple API to generate QR codes.",
            version="1.0.0",
        )

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI is running!"}

@app.get("/ping")
def read_root():
    return {"message": "🚀 FastAPI is running!"}

app.include_router(qrcode.router, prefix= "/v1", tags=["QR Code"])
