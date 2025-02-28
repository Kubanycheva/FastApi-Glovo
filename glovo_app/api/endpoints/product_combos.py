from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import ProductComboSchema
from glovo_app.db.models import ProductCombo


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

product_combo_router = APIRouter(prefix='/product_combo', tags=['ProductCombo'])


@product_combo_router.post('/create', response_model=ProductComboSchema)
async def create_product_combo(combo: ProductComboSchema, db: Session = Depends(get_db)):
    db_combo = ProductCombo(**combo.dict())
    db.add(db_combo)
    db.commit()
    db.refresh(db_combo)
    return db_combo


@product_combo_router.get('/', response_model=List[ProductComboSchema])
async def list_combo(db: Session = Depends(get_db)):
    return db.query(ProductCombo).all()


@product_combo_router.get('/{product_combo_id}/', response_model=ProductComboSchema)
async def detail_combo(combo_id: int, db: Session = Depends(get_db)):
    combo = db.query(ProductCombo).filter(ProductCombo.id == combo_id).first()
    if combo is None:
        raise HTTPException(status_code=404, detail='ProductCombo Not Found')
    return combo


@product_combo_router.put('/update', response_model=ProductComboSchema)
async def update_combo(combo_id: int, combo_data: ProductComboSchema, db: Session = Depends(get_db)):
    combo = db.query(ProductCombo).filter(ProductCombo.id == combo_id).first()
    if combo is None:
        raise HTTPException(status_code=404, detail='ProductCombo Not Found')
    return combo

    for combo_key, combo_value in combo_data.dict().items():
        setattr(combo, combo_key, combo_value)
    db.commit()
    db.refresh(combo)
    return combo


@product_combo_router.delete('/delete')
async def delete_combo(combo_id: int, db: Session = Depends(get_db)):
    combo = db.query(ProductCombo).filter(ProductCombo.id == combo_id).first()
    if combo is None:
        raise HTTPException(status_code=404, detail='ProductCombo Not Found')
    db.delete(combo)
    db.commit()
    return {'message': 'This ProductCombo is deleted'}

