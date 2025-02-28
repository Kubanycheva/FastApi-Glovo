from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import StoreReviewSchema
from glovo_app.db.models import StoreReview


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

store_review_router = APIRouter(prefix='/store_review', tags=['StoreReview'])


@store_review_router.post('/create', response_model=StoreReviewSchema)
async def create_review(review: StoreReviewSchema, db: Session = Depends(get_db)):
    db_review = StoreReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@store_review_router.get('/', response_model=StoreReviewSchema)
async def list_review(db: Session = Depends(get_db)):
    return db.query(StoreReview).all()


@store_review_router.get('/{store_review_id}', response_model=StoreReviewSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='StoreReview Not Found')
    return review


@store_review_router.put('/update', response_model=StoreReviewSchema)
async def update_review(review_id: int, review_data: StoreReviewSchema, db: Session = Depends(get_db)):
    review = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='StoreReview Not Found')
    return review

    for review_key, review_value in review_data.dict().items():
        setattr(review, review_key, review_value)
    db.commit()
    db.refresh(review)
    return review


@store_review_router.delete('/delete')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='StoreReview Not Found')
    db.delete(review)
    db.commit()
    return {'message': 'This StoreReview is deleted'}

