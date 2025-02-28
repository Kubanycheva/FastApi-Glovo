from fastapi import FastAPI
from sqladmin import Admin
from .views import (CartAdmin, CartItemAdmin, CategoryAdmin, StoreAdmin, StoreReviewAdmin,
                    ContactInfoAdmin, ProductAdmin, ProductComboAdmin, CourierAdmin, CourierReviewAdmin,
                    OrderAdmin, UserProfileAdmin)
from glovo_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)
    admin.add_view(CourierAdmin)
    admin.add_view(StoreReviewAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductComboAdmin)
    admin.add_view(ContactInfoAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(CourierReviewAdmin)
