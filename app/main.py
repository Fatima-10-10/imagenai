from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware.logging_middleware import log_requests
from app.cache import get_from_cache, set_in_cache

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

@app.get("/test-cache")
def test_cache(prompt: str):
    cached = get_from_cache(prompt)
    if cached:
        return {"source": "cache", "result": cached}
    
    result = f"Generated image for: {prompt}"
    set_in_cache(prompt, result)
    return {"source": "api", "result": result}