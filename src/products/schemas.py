import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from src.reviews.schemas import ReviewModel


class Product(BaseModel):
    puid: uuid.UUID
    name: str
    unit: str
    retail_price: float
    cost_price: float
    supplier: str
    manufacturer: str
    created_at: datetime
    updated_at: datetime


class ProductDetailModel(Product):
    reviews: List[ReviewModel]
    pass


class ProductCreateModel(BaseModel):
    name: str
    unit: str
    retail_price: float
    cost_price: float
    supplier: str
    manufacturer: str


class ProductUpdateModel(BaseModel):
    name: str
    unit: str
    retail_price: float
    cost_price: float
    supplier: str
    manufacturer: str
