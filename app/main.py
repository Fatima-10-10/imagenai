from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response
from app.middleware.logging_middleware import log_requests
from app.cache import get_from_cache, set_in_cache
from app.image_service import generate_image
from app.cache import get_from_cache, set_in_cache, get_cache_stats

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

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/test-cache")
def test_cache(prompt: str):
    cached = get_from_cache(prompt)
    if cached:
        return {"source": "cache", "result": cached}
    
    result = f"Generated image for: {prompt}"
    set_in_cache(prompt, result)
    return {"source": "api", "result": result}

@app.get("/generate")
async def generate(prompt: str = Query(..., description="Text prompt for image generation")):
    cached = get_from_cache(prompt)
    if cached:
        return Response(content=cached, media_type="image/png")
    
    image_bytes = await generate_image(prompt)
    set_in_cache(prompt, image_bytes)
    return Response(content=image_bytes, media_type="image/png")

@app.get("/cache-stats")
def cache_stats():
    return get_cache_stats()    