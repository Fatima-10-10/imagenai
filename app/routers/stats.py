from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ImageRequest
from datetime import datetime, date

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(ImageRequest).count()
    completed = db.query(ImageRequest).filter(ImageRequest.status == "COMPLETED").count()
    failed = db.query(ImageRequest).filter(ImageRequest.status == "FAILED").count()
    queued = db.query(ImageRequest).filter(ImageRequest.status == "QUEUED").count()
    
    today = date.today()
    today_total = db.query(ImageRequest).filter(
        ImageRequest.created_at >= datetime.combine(today, datetime.min.time())
    ).count()
    
    return {
        "total_requests": total,
        "completed": completed,
        "failed": failed,
        "queued": queued,
        "today": today_total
    }