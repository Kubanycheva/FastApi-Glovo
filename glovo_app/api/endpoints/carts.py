from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CartSchema, CartItemSchema, ProductSchema, CartItemCreateSchema
from glovo_app.db.models import Cart, CartItem, Product


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

cart_router = APIRouter(prefix='/cart', tags=['Cart'])


@cart_router.post('/create', response_model=CartItemSchema)
async def create_cart(user_id: int, item_data: CartItemCreateSchema,
                      db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product Not Found')

    product_item = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                              CartItem.product_id == item_data.product_id).first()
    if product_item:
        raise HTTPException(status_code=404, detail='Product already in cart')

    cart_item = CartItem(cart_id=cart.id, product_id=item_data.product_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


@cart_router.get('/', response_model=CartSchema)
async def cart_list(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Корзина не найдена')

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    total_price = sum(db.query(Product.price).filter(Product.id == item.product_id).scalar() for item in cart_items)
    return {
        'id': cart.id,
        'user_id': cart.user_id,
        'items': cart.items,
        'total_price': total_price
    }


@cart_router.delete('/{product_id}')
async def delete_cart(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')

    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                                          CartItem.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail='Product absent in cart')
    db.delete(cart_item)
    db.commit()
    return {'message': 'Product deleted from cart'}

