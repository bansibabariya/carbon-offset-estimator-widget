from pydantic import BaseModel
from typing import List, Optional


class CartItem(BaseModel):
    id: int
    title: str
    price: float
    quantity: int = 1
    weight: Optional[float] = None
    category: Optional[str] = None


class EstimateRequest(BaseModel):
    cart: List[CartItem]
    currency: Optional[str] = "USD"


class EstimateResponse(BaseModel):
    estimated_offset: float
    breakdown: List[dict]


class OptInRequest(BaseModel):
    merchant_id: str
    customer_email: Optional[str]
    customer_name: Optional[str]
    cart: List[CartItem]
    estimated_offset: float
