from sqlalchemy import Column, String, DateTime, Text
from app.database import Base
from datetime import datetime
import uuid

class ImageRequest(Base):
    __tablename__ = "image_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = Column(Text, nullable=False)
    status = Column(String, default="QUEUED")
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)