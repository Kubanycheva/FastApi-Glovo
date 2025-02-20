from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models import TypeChoices, StatusChoices, RoleChoices


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    phone_number: Optional[str] = None
    role: RoleChoices

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class StoreSchema(BaseModel):
    id: int
    store_name: str
    store_image: str
    category_id: int
    description: str
    address: str
    owner_id: int

    class Config:
        from_attributes = True


class ContactInfoSchema(BaseModel):
    id: int
    contact_info: str
    store_id: int

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    product_name: str
    product_image: str
    price: int
    description: str

    class Config:
        from_attributes = True


class ProductComboSchema(BaseModel):
    id: int
    combo_name: str
    combo_image: str
    price: float
    description: str
    store_id: int

    class Config:
        from_attribute = True


class CartSchema(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attribute = True


class CartItemSchema(BaseModel):
    id: int
    cart_id: int
    product: int
    quantity: int


class StoreReviewSchema(BaseModel):
    id: int
    client: str
    store: int
    rating: int
    comment: str
    created_date: int

    class Config:
        from_attribute = True


class CourierReviewSchema(BaseModel):
    id: int
    client: int
    courier: int
    rating: int
    created_date: int

    class Config:
        from_attribute = True


class OrderSchema(BaseModel):
    id: int
    status: StatusChoices
    delivery_address: int
    created_date: datetime

    class Config:
        from_attributes = True


class CourierSchema(BaseModel):
    id: int
    type: TypeChoices

    class Config:
        from_attributes = True
