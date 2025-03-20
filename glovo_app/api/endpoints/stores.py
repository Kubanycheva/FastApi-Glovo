from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Query
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import StoreSchema
from glovo_app.db.models import Store, Category


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
store_router = APIRouter(prefix='/store', tags=['Store'])


@store_router.get('/search/', response_model=List[StoreSchema])
async def search_product(store_name: str, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.store_name.ilike(f'%{store_name}%')).all()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Store Not Found')
    return store_db


@store_router.post('/create/', response_model=StoreSchema)
async def create_store(store: StoreSchema, db: Session = Depends(get_db)):
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@store_router.get('/', response_model=List[StoreSchema])
async def list_product(category_name: Optional[str] = None, db: Session = Depends(get_db)):

    store = db.query(Store).join(Category).filter(Category.category_name == category_name)
    if not store:
        raise HTTPException(status_code=404, detail='Store Not Found')
    return store


@store_router.get('/{store_id}/', response_model=StoreSchema)
async def detail_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Store Not Found')
    return store


@store_router.put('/{store_id}/', response_model=StoreSchema)
async def update_store(store_id: int, store_data: StoreSchema,  db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Store Not Found')

    for store_key, store_value in store_data.dict().items():
        setattr(store, store_key, store_value)
    db.commit()
    db.refresh(store)
    return store


@store_router.delete('/{store_id}/')
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Store Not Found')
    db.delete(store)
    return {'message': 'This store is deleted'}