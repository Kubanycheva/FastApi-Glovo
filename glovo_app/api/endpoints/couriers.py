from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CourierSchema
from glovo_app.db.models import Courier


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

courier_router = APIRouter(prefix='/courier', tags=['Courier'])


@courier_router.post('/create', response_model=CourierSchema)
async def create_courier(courier: CourierSchema, db: Session = Depends(get_db)):
    db_courier = Courier(**courier.dict())
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier


@courier_router.get('/', response_model=List[CourierSchema])
async def list_courier(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/{courier_id}', response_model=CourierSchema)
async def detail_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='Courier Not Found')
    return courier


@courier_router.put('/update', response_model=CourierSchema)
async def update_courier(courier_id: int, courier_data: CourierSchema, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='Courier Not Found')
    return courier

    for courier_key, courier_value in courier_data.dict().items():
        setattr(courier, courier_key, courier_value)
    db.commit()
    db.refresh(courier)
    return courier


@courier_router.delete('/delete')
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='Courier Not Found')
    db.delete(courier)
    db.commit()
    return {'message': 'This Courier is deleted'}

