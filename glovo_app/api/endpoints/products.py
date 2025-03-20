from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Query
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import ProductSchema
from glovo_app.db.models import Product

from sqlalchemy import asc, desc
from fastapi_pagination import Page, add_pagination, paginate


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

product_router = APIRouter(prefix='/product', tags=['Product'])


@product_router.get('/search/', response_model=List[ProductSchema])
async def search_product(product_name: str, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.product_name.ilike(f'%{product_name}%')).all()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product_db


@product_router.post('/create/', response_model=ProductSchema)
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@product_router.get('/', response_model=Page[ProductSchema],)
async def list_product(min_price: Optional[float] = Query(None, alias='price[from]'),
                       max_price: Optional[float] = Query(None, alias='price[to]'),
                       order_by: Optional[str] = Query(None, regex='^(asc|desc)$'),

                       db: Session = Depends(get_db)):

    query = db.query(Product)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if order_by == 'asc':
        query = query.order_by(asc(Product.price))
    elif order_by == 'desc':
        query = query.order_by(desc(Product.price))

    products = query.all()

    if products is None:
        raise HTTPException(status_code=404, detail='Product Not Found')

    return paginate(products)


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

