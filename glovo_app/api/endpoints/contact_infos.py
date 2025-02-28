from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import ContactInfoSchema
from glovo_app.db.models import ContactInfo


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

contact_info_router = APIRouter(prefix='/contact_info', tags=['ContactInfo'])


@contact_info_router.post('/create/', response_model=ContactInfoSchema)
async def create_contact(contact: ContactInfoSchema, db: Session = Depends(get_db)):
    db_contact = ContactInfo(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@contact_info_router.get('/', response_model=List[ContactInfoSchema])
async def list_contact(db: Session = Depends(get_db)):
    return db.query(ContactInfo).all()


@contact_info_router.get('/{contact_id}', response_model=ContactInfoSchema)
async def detail_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactInfo).filter(ContactInfo.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail='ContactInfo Not Found')
    return contact


@contact_info_router.put('/{contact_id}/', response_model=ContactInfoSchema)
async def update_contact(contact_id: int, contact_data: ContactInfoSchema,
                        db: Session = Depends(get_db)):
    contact = db.query(ContactInfo).filter(ContactInfo.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail='ContactInfo Not Found')
    return contact

    for contact_key, contact_value in contact_data.dict().items():
        setattr(contact, contact_key, contact_value)
    db.commit()
    db.refresh(contact)
    return contact


@contact_info_router.delete('/{contact_info.id}/')
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactInfo).filter(ContactInfo.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail='ContactInfo Not Found')
    db.delete(contact)
    db.commit()
    return {'message': 'This ContactInfo is deleted'}

