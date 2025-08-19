from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from .db import Base

class OptIn(Base):
    __tablename__ = 'optins'
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, nullable=False) 
    customer_email = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    estimated_offset = Column(Float, nullable=False)
    cart_snapshot = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
