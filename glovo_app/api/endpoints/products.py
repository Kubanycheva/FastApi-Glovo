from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import ProductSchema
from glovo_app.db.models import Product

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

product_router = APIRouter(prefix='/product', tags=['Product'])


@product_router.post('/create/', response_model=ProductSchema)
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@product_router.get('/', response_model=List[ProductSchema],)
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}/', response_model=ProductSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product


@product_router.put('/update/', response_model=ProductSchema)
async def update_product(product_id: int, product_data: ProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product

    for product_key, product_value in product_data.dict().items():
        setattr(product, product_key, product_value)
    db.commit()
    db.refresh(product)
    return product


@product_router.delete('/{product.id}/')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    db.delete(product)
    db.commit()
    return {'message': 'This Product is deleted'}

