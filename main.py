import fastapi
from models import (Category, Store, ContactInfo, UserProfile, RefreshToken,
                    Product, Order, Courier, ProductCombo, Cart, CartItem, StoreReview, CourierReview)
from schema import (CategorySchema, StoreSchema, ContactInfoSchema, UserProfileSchema,
                    ProductSchema, OrderSchema, CourierSchema, ProductComboSchema, CartSchema, CartItemSchema, StoreReviewSchema,
                    CourierReviewSchema)
from database import SessionLocal, engine
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from schema import *
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta

from sqladmin import Admin, ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]
    name = 'User'
    name_plural = 'Users'


glovo_app = fastapi.FastAPI(title='Glovo site')

admin = Admin(glovo_app, engine)

admin.add_view(UserProfileAdmin)

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


@glovo_app.post('/register', tags=['Регистрация'])
async def register(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=404, detail='username бар экен')
    new_hash_pass = get_password_hash(user.password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        role=user.role,
        hashed_password=new_hash_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'Saved'}


@glovo_app.post('/login', tags=['Регистрация'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Маалымат туура эмес')
    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})
    token_db = RefreshToken(token=refresh_token, user_id=user.id)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@glovo_app.post('/logout', tags=['Регистрация'])
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()
    return {'message': 'Вышли'}


@glovo_app.post('/refresh', tags=['Регистрация'])
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_entry = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_entry:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    access_token = create_access_token({'sub': token_entry.user_id})

    return {'access_token': access_token, 'token_type': 'bearer'}


@glovo_app.post('/category/create/', response_model=CategorySchema, tags=['Category'])
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@glovo_app.get('/category/', response_model=List[CategorySchema], tags=['Category'])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@glovo_app.get('/category/{category_id}/', response_model=CategorySchema, tags=['Category'])
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    return category


@glovo_app.put('/category/{category_id/', response_model=CategorySchema, tags=['Category'])
async def update_category(category_id: int, category_data: CategorySchema,
                          db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    category.category_name = category_data.category_name
    db.commit()
    db.refresh(category)
    return category


@glovo_app.delete('/category/{category_id}', response_model=CategorySchema, tags=['Category'])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    db.delete(category)
    db.commit()
    return {'message': 'Category deleted successfully'}


@glovo_app.post('/store/create/', response_model=StoreSchema, tags=['Store'])
async def create_store(store: StoreSchema, db: Session = Depends(get_db)):
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@glovo_app.get('/store/', response_model=List[StoreSchema], tags=['Store'])
async def list_store(db: Session = Depends(get_db)):
    return db.query(Store).all()


@glovo_app.get('/store/{store_id}/', response_model=StoreSchema, tags=['Store'])
async def detail_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Store Not Found')
    return store


@glovo_app.put('/store/{store_id}/', response_model=StoreSchema, tags=['Store'])
async def update_store(store_id: int, store_data: StoreSchema,  db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Store Not Found')

    for store_key, store_value in store_data.dict().items():
        setattr(store, store_key, store_value)
    db.commit()
    db.refresh(store)
    return store


@glovo_app.delete('/store{store_id}/', tags=['Store'])
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Store Not Found')
    db.delete(store)
    return {'message': 'This store is deleted'}


@glovo_app.post('/contact/create/', response_model=ContactInfoSchema, tags=['ContactInfo'])
async def create_contact(contact: ContactInfoSchema, db: Session = Depends(get_db)):
    db_contact = ContactInfo(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@glovo_app.get('/contact/', response_model=List[ContactInfoSchema], tags=['ContactInfo'])
async def list_contact(db: Session = Depends(get_db)):
    return db.query(ContactInfo).all()


@glovo_app.get('/contact/{contact_id}', response_model=ContactInfoSchema, tags=['ContactInfo'])
async def detail_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactInfo).filter(ContactInfo.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail='ContactInfo Not Found')
    return contact


@glovo_app.put('/contact/{contact_id}/',response_model=ContactInfoSchema,  tags=['ContactInfo'])
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


@glovo_app.delete('/contact/{contact_info.id}/', tags=['ContactInfo'])
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactInfo).filter(ContactInfo.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail='ContactInfo Not Found')
    db.delete(contact)
    db.commit()
    return {'message': 'This ContactInfo is deleted'}


@glovo_app.post('/product/create/', tags=['Product'])
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@glovo_app.get('/product/', response_model=List[ProductSchema], tags=['Product'])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@glovo_app.get('/product/{product_id}/', response_model=ProductSchema, tags=['Product'])
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product


@glovo_app.put('/product/update/', response_model=ProductSchema, tags=['Product'])
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


@glovo_app.delete('/product/{product.id}/', tags=['Product'])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    db.delete(product)
    db.commit()
    return {'message': 'This Product is deleted'}


@glovo_app.post('/product_combo/create', response_model=ProductComboSchema, tags=['ProductCombo'])
async def create_product_combo(combo: ProductComboSchema, db: Session = Depends(get_db)):
    db_combo = ProductCombo(**combo.dict())
    db.add(db_combo)
    db.commit()
    db.refresh(db_combo)
    return db_combo


@glovo_app.get('/product_combo', response_model=ProductComboSchema, tags=['ProductCombo'])
async def list_combo(db: Session = Depends(get_db)):
    return db.query(ProductCombo).all()


@glovo_app.get('/product_combo{product_combo_id}/', response_model=ProductComboSchema, tags=['ProductCombo'])
async def detail_combo(combo_id: int, db: Session = Depends(get_db)):
    combo = db.query(ProductCombo).filter(ProductCombo.id == combo_id).first()
    if combo is None:
        raise HTTPException(status_code=404, detail='ProductCombo Not Found')
    return combo


@glovo_app.put('/product_combo/update', response_model=ProductComboSchema, tags=['ProductCombo'])
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


@glovo_app.delete('/product_combo/delete', tags=['ProductCombo'])
async def delete_combo(combo_id: int, db: Session = Depends(get_db)):
    combo = db.query(ProductCombo).filter(ProductCombo.id == combo_id).first()
    if combo is None:
        raise HTTPException(status_code=404, detail='ProductCombo Not Found')
    db.delete(combo)
    db.commit()
    return {'message': 'This ProductCombo is deleted'}


@glovo_app.post('/cart/create', response_model=CartSchema, tags=['Cart'])
async def create_cart(cart: CartSchema, db: Session = Depends(get_db)):
    db_cart = Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


@glovo_app.get('/cart', response_model=CartSchema, tags=['Cart'])
async def list_cart(db: Session = Depends(get_db)):
    return db.query(Cart).all()


@glovo_app.get('/cart/{cart_id}', response_model=CartSchema, tags=['Cart'])
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    return cart


@glovo_app.put('/cart/update', response_model=CartSchema, tags=['Cart'])
async def update_cart(cart_id: int, cart_data: CartSchema, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    return cart

    for cart_key, cart_value in cart_data.dict().items():
        setattr(cart, cart_key, cart_value)
        db.commit()
        db.refresh(cart)
        return cart


@glovo_app.delete('/cart/delete', tags=['Cart'])
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail='Cart Not Found')
    db.delete(cart)
    db.commit()
    return {'message': 'This Cart is deleted'}


@glovo_app.post('store_review/create', response_model=StoreReviewSchema, tags=['StoreReview'])
async def create_review(review: StoreReviewSchema, db: Session = Depends(get_db)):
    db_review = StoreReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@glovo_app.get('/store_review/', response_model=StoreReviewSchema, tags=['StoreReview'])
async def list_review(db: Session = Depends(get_db)):
    return db.query(StoreReview).all()


@glovo_app.get('/store_review/{store_review_id}', response_model=StoreReviewSchema, tags=['StoreReview'])
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='StoreReview Not Found')
    return review


@glovo_app.put('/store_review/update', response_model=StoreReviewSchema, tags=['StoreReview'])
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


@glovo_app.delete('/store_review/delete', tags=['StoreReview'])
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='StoreReview Not Found')
    db.delete(review)
    db.commit()
    return {'message': 'This StoreReview is deleted'}


@glovo_app.post('courier/create', response_model=CourierSchema, tags=['Courier'])
async def create_courier(courier: CourierSchema, db: Session = Depends(get_db)):
    db_courier = Courier(**courier.dict())
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier


@glovo_app.get('/courier/', response_model=CourierSchema, tags=['Courier'])
async def list_courier(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@glovo_app.get('/courier/{courier_id}', response_model=CourierSchema, tags=['Courier'])
async def detail_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='Courier Not Found')
    return courier


@glovo_app.put('/courier/update', response_model=CourierSchema, tags=['Courier'])
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


@glovo_app.delete('/courier/delete', tags=['Courier'])
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='Courier Not Found')
    db.delete(courier)
    db.commit()
    return {'message': 'This Courier is deleted'}


@glovo_app.post('courier_review/create', response_model=CourierReviewSchema, tags=['CourierReview'])
async def create_courier_review(courier_review: CourierReviewSchema, db: Session = Depends(get_db)):
    db_courier_review = CourierReview(**courier_review.dict())
    db.add(db_courier_review)
    db.commit()
    db.refresh(db_courier_review)
    return db_courier_review


@glovo_app.get('/courier_review/', response_model=CourierReviewSchema, tags=['CourierReview'])
async def list_courier_review(db: Session = Depends(get_db)):
    return db.query(CourierReview).all()


@glovo_app.get('/courier_review/{courier_review_id}', response_model=CourierReviewSchema, tags=['CourierReview'])
async def detail_review(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='CourierReview Not Found')
    return courier_review


@glovo_app.put('/courier_review/update', response_model=CourierReviewSchema, tags=['CourierReview'])
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


@glovo_app.delete('/courier_review/delete', tags=['CourierReview'])
async def delete_courier_review(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='CourierReview Not Found')
    db.delete(courier_review)
    db.commit()
    return {'message': 'This CourierReview is deleted'}


@glovo_app.post('/order/create', response_model=OrderSchema, tags=['Order'])
async def create_product(order: OrderSchema, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@glovo_app.get('/order/', response_model=OrderSchema, tags=['Order'])
async def list_order(db: Session = Depends(get_db)):
    return db.query(Order).all()


@glovo_app.get('/order/{order_id}/',response_model=OrderSchema, tags=['Order'])
async def detail_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    return order


@glovo_app.put('/order/update', response_model=OrderSchema, tags=['Order'])
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


@glovo_app.delete('/order/delete', tags=['Order'])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    db.delete(order)
    db.commit()
    return {'message': 'This Order is deleted'}














@glovo_app.post('/item/create', response_model=CartItemSchema, tags=['CartItem'])
async def create_item(item: CartItemSchema, db: Session = Depends(get_db)):
    db_item = Cart(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@glovo_app.get('/item/', response_model=CartItemSchema, tags=['CartItem'])
async def list_item(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@glovo_app.get('/item/{item_id}/',response_model=CartItemSchema, tags=['CartItem'])
async def detail_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='CartItem Not Found')
    return item


@glovo_app.put('/item/update', response_model=CartItemSchema, tags=['CartItem'])
async def update_order(order_id: int, order_data: OrderSchema, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='CartItem Not Found')
    return order

    for order_key, order_value in order_data.dict().items():
        setattr(order, order_key, order_value)
        db.commit()
        db.refresh(order)
        return order


@glovo_app.delete('/order/delete', tags=['Order'])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    db.delete(order)
    db.commit()
    return {'message': 'This Order is deleted'}

