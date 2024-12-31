import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.products.schemas import Product

from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    mobile_number: str = Field(max_length=11)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "mobile_number": "03331212121",
                "password": "testpass123",
            }
        }
    }


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    mobile_number: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime


class UserProductModel(UserModel):
    products: List[Product]
    # reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
