from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import OrderSchema
from glovo_app.db.models import Order


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

order_router = APIRouter(prefix='/order', tags=['Order'])


@order_router.post('/create', response_model=OrderSchema)
async def create_product(order: OrderSchema, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@order_router.get('/', response_model=OrderSchema)
async def list_order(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/{order_id}/',response_model=Order`Schema)
async def detail_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    return order


@order_router.put('/update', response_model=OrderSchema)
async def update_order(order_id: int, order_data: OrderSchema, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    return order

    for order_key, order_value in order_data.dict().items():
        setattr(order, order_key, order_value)
    db.commit()
    db.refresh(order)
    return order


@order_router.delete('/delete')
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    db.delete(order)
    db.commit()
    return {'message': 'This Order is deleted'}
