from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ImageRequest

router = APIRouter()

@router.get("/status/{request_id}")
def get_status(request_id: str, db: Session = Depends(get_db)):
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {
        "request_id": str(request.id),
        "prompt": request.prompt,
        "status": request.status,
        "created_at": request.created_at,
        "completed_at": request.completed_at
    }

@router.get("/image/{request_id}")
def get_image(request_id: str, db: Session = Depends(get_db)):
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != "COMPLETED":
        raise HTTPException(status_code=400, detail=f"Image not ready, status: {request.status}")
    
    return FileResponse(request.image_path, media_type="image/png")