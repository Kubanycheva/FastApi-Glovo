from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CourierReviewSchema
from glovo_app.db.models import CourierReview


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

courier_review_router = APIRouter(prefix='/courier_review', tags=['CourierReview'])


@courier_review_router.post('/create', response_model=CourierReviewSchema)
async def create_courier_review(courier_review: CourierReviewSchema, db: Session = Depends(get_db)):
    db_courier_review = CourierReview(**courier_review.dict())
    db.add(db_courier_review)
    db.commit()
    db.refresh(db_courier_review)
    return db_courier_review


@courier_review_router.get('/', response_model=CourierReviewSchema)
async def list_courier_review(db: Session = Depends(get_db)):
    return db.query(CourierReview).all()


@courier_review_router.get('/{courier_review_id}', response_model=CourierReviewSchema)
async def detail_review(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='CourierReview Not Found')
    return courier_review


@courier_review_router.put('/update', response_model=CourierReviewSchema)
async def update_review(courier_review_id: int, courier_review_data: CourierReviewSchema, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='CourierReview Not Found')
    return courier_review

    for courier_review_key, courier_review_value in courier_review_data.dict().items():
        setattr(courier_review, courier_review_key, courier_review_value)
    db.commit()
    db.refresh(courier_review)
    return courier_review


@courier_review_router.delete('/delete')
async def delete_courier_review(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='CourierReview Not Found')
    db.delete(courier_review)
    db.commit()
    return {'message': 'This CourierReview is deleted'}
