from sqlalchemy import String, Enum, DECIMAL, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from glovo_app.db.database import Base
from enum import Enum as PyEnum
from passlib.hash import bcrypt


class TypeChoices(str, PyEnum):
    available = 'available'
    busy = 'busy'


class StatusChoices(str, PyEnum):
    str1 = 'Ожидает обработки'
    str2 = 'В процессе доставки'
    str3 = 'Доставлен'
    str4 = 'Отменен'


class RoleChoices(str, PyEnum):
    client = 'client'
    courier = 'courier'
    admin = 'admin'


class UserProfile(Base):
    __tablename__ = 'userprofile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(40), unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), nullable=False, default=RoleChoices.client)
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user')

    cart_user: Mapped['UserProfile'] = relationship('Cart', back_populates='users', cascade='all, delete-orphan',
                                                    uselist=False)

    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    stores: Mapped[List['Store']] = relationship('Store', back_populates='category')


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    store_name: Mapped[str] = mapped_column(String(32))
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id')) #*
    category: Mapped['Category'] = relationship('Category', back_populates='stores') #*

    description: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String(64))
    owner_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))


class ContactInfo(Base):
    __tablename__ = 'contact_info'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    contact_info: Mapped[str | None] = mapped_column(String, nullable=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String(32))
    product_image: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    description: Mapped[str] = mapped_column(Text)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))


class ProductCombo(Base):
    __tablename__ = 'product_combo'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    combo_name: Mapped[str] = mapped_column(String(32), unique=True)
    combo_image: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    description: Mapped[str] = mapped_column(String)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))


class Cart(Base):
    __tablename__ = 'cart'
    
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'), unique=True)
    users: Mapped['UserProfile'] = relationship('UserProfile', back_populates='cart_user')

    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship('Product')
    quantity: Mapped[int] = mapped_column(Integer, default=1)


class StoreReview(Base):
    __tablename__ = 'store_review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    client: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    store: Mapped[int] = mapped_column(ForeignKey('store.id'))
    rating: Mapped[DECIMAL] = mapped_column(DECIMAL(1, 6))
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CourierReview(Base):
    __tablename__ = 'courier_review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    client: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    courier: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    rating: Mapped[DECIMAL] = mapped_column(DECIMAL(1, 6))
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ ='order'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), nullable=False, default=StatusChoices.str1)
    delivery_address: Mapped[str] = mapped_column(String(64))
    courier_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    created_date: Mapped[int] = mapped_column(DateTime, default=datetime.utcnow)


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    current_orders_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    type: Mapped[TypeChoices] = mapped_column(Enum(TypeChoices), nullable=False, default=TypeChoices.available)






