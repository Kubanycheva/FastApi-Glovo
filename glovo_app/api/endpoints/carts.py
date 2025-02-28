from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CartSchema
from glovo_app.db.models import Cart


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

cart_router = APIRouter(prefix='/cart', tags=['Cart'])


@cart_router.post('/create', response_model=CartSchema)
async def create_cart(cart: CartSchema, db: Session = Depends(get_db)):
    db_cart = Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


@cart_router.get('/', response_model=CartSchema)
async def list_cart(db: Session = Depends(get_db)):
    return db.query(Cart).all()


@cart_router.get('/{cart_id}', response_model=CartSchema)
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    return cart


@cart_router.put('/update', response_model=CartSchema)
async def update_cart(cart_id: int, cart_data: CartSchema, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    return cart

    for cart_key, cart_value in cart_data.dict().items():
        setattr(cart, cart_key, cart_value)
    db.commit()
    db.refresh(cart)
    return cart


@cart_router.delete('/delete')
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    db.delete(cart)
    db.commit()
    return {'message': 'This Cart is deleted'}
