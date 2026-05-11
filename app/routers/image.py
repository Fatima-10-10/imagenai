from fastapi import APIRouter, Query
from fastapi.responses import Response
from app.cache import get_from_cache, set_in_cache, get_cache_stats
from app.image_service import generate_image

router = APIRouter()

@router.get("/generate")
async def generate(prompt: str = Query(..., description="Text prompt for image generation")):
    cached = get_from_cache(prompt)
    if cached:
        return Response(content=cached, media_type="image/png")
    
    image_bytes = await generate_image(prompt)
    set_in_cache(prompt, image_bytes)
    return Response(content=image_bytes, media_type="image/png")

@router.get("/cache-stats")
def cache_stats():
    return get_cache_stats()

@router.get("/test-cache")
def test_cache(prompt: str):
    cached = get_from_cache(prompt)
    if cached:
        return {"source": "cache", "result": cached}
    
    result = f"Generated image for: {prompt}"
    set_in_cache(prompt, result)
    return {"source": "api", "result": result}