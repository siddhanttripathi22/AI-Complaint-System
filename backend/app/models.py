
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    complaint_source = Column(String(255))
    customer_name = Column(String(255))

    
    product_name = Column(String(255))
    product_strength = Column(String(255))
    batch_number = Column(String(255))
    manufacturing_date = Column(String(100))
    expiry_date = Column(String(100))
    quantity_affected = Column(String(100))

   
    complaint_type = Column(String(255))
    complaint_date = Column(String(100))
    description = Column(Text)

   
    initial_severity = Column(String(100))
    priority = Column(String(100))

    
    ai_summary = Column(Text)
    ai_risk = Column(String(100))

    status = Column(String(50), default="Pending Triage")
    created_at = Column(DateTime, default=datetime.utcnow)
