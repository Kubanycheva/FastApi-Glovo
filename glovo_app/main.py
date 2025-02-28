import fastapi
from api.endpoints import (auth, categories, orders, carts, cart_items, contact_infos, couriers, courier_reviews,
                           store_reviews, stores, users, products, product_combos, users)

import redis.asyncio as redis
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter

import uvicorn

from glovo_app.admin.setup import setup_admin


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8',
                                decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


glovo_app = fastapi.FastAPI(title='Glovo site', lifespan=lifespan)
setup_admin(glovo_app)

glovo_app.include_router(auth.auth_router, tags=['Auth'])
glovo_app.include_router(users.user_router, tags=['UserProfile'])
glovo_app.include_router(categories.category_router, tags=['Category'])
glovo_app.include_router(cart_items.cart_item, tags=['CartItem'])
glovo_app.include_router(carts.cart_router, tags=['Cart'])
glovo_app.include_router(orders.order_router, tags=['Order'])
glovo_app.include_router(products.product_router, tags=['Product'])
glovo_app.include_router(store_reviews.store_review_router, tags=['StoreReview'])
glovo_app.include_router(stores.store_router, tags=['Store'])
glovo_app.include_router(contact_infos.contact_info_router, tags=['ContactInfo'])
glovo_app.include_router(couriers.courier_router, tags=['Courier'])
glovo_app.include_router(courier_reviews.courier_review_router, tags=['CourierReview'])
glovo_app.include_router(product_combos.product_combo_router, tags=['ProductCombo'])


if __name__ == '__main__':
    uvicorn.run(glovo_app, host='127.0.0.1', port=8000)









