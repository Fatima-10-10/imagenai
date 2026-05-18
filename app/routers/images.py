from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ImageRequest

router = APIRouter()

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    requests = db.query(ImageRequest).order_by(ImageRequest.created_at.desc()).all()
    
    return [
        {
            "request_id": str(r.id),
            "prompt": r.prompt,
            "status": r.status,
            "created_at": r.created_at,
            "completed_at": r.completed_at
        }
        for r in requests
    ]

@router.delete("/image/{request_id}")
def delete_image(request_id: str, db: Session = Depends(get_db)):
    request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    import os
    if request.image_path and os.path.exists(request.image_path):
        os.remove(request.image_path)
    
    db.delete(request)
    db.commit()
    
    return {"message": "Image deleted successfully"}