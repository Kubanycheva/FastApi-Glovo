from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CartItemSchema
from glovo_app.db.models import CartItem


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

cart_item = APIRouter(prefix='/cart_item', tags=['CartItem'])


@cart_item.post('/create', response_model=CartItemSchema)
async def create_item(item: CartItemSchema, db: Session = Depends(get_db)):
    db_item = CartItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@cart_item.get('/', response_model=CartItemSchema)
async def list_item(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@cart_item.get('/{item_id}/',response_model=CartItemSchema)
async def detail_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='CartItem Not Found')
    return item


@cart_item.put('/update', response_model=CartItemSchema)
async def update_item(item_id: int, item_data: CartItemSchema, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='CartItem Not Found')
    return item

    for item_key, item_value in item_data.dict().items():
        setattr(item, item_key, item_value)
    db.commit()
    db.refresh(item)
    return item


@cart_item.delete('/delete')
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='CartItem Not Found')
    db.delete(item)
    db.commit()
    return {'message': 'This CartItem is deleted'}
