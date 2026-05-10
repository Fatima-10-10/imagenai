from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware.logging_middleware import log_requests

app = FastAPI(
    title="ImagenAI",
    description="AI Image Generation App",
    version="1.0.0"
)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "Welcome to ImagenAI"}