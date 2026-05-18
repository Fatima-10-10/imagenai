from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware.logging_middleware import log_requests
from app.database import engine
from app import models
from app.routers import generate, status, images, stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ImagenAI",
    description="AI Image Generation App",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(generate.router)
app.include_router(status.router)
app.include_router(images.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return FileResponse("app/static/index.html")