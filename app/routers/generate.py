from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ImageRequest
from app.image_service import generate_image
import uuid
import os

router = APIRouter()

async def process_image(request_id: str, prompt: str):
    db = next(get_db())
    try:
        image_bytes = await generate_image(prompt)
        
        os.makedirs("generated_images", exist_ok=True)
        image_path = f"generated_images/{request_id}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        
        request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
        request.status = "COMPLETED"
        request.image_path = image_path
        from datetime import datetime
        request.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        request = db.query(ImageRequest).filter(ImageRequest.id == request_id).first()
        request.status = "FAILED"
        db.commit()
    finally:
        db.close()

@router.post("/generate")
async def generate(prompt: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    
    new_request = ImageRequest(
        id=request_id,
        prompt=prompt,
        status="QUEUED"
    )
    db.add(new_request)
    db.commit()
    
    background_tasks.add_task(process_image, request_id, prompt)
    
    return {
        "request_id": request_id,
        "status": "QUEUED",
        "message": "Image generation started"
    }