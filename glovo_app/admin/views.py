from sqladmin import ModelView
from glovo_app.db.models import (UserProfile, Category, Cart, CartItem, Courier, CourierReview, Order,
                                 ContactInfo, Product, ProductCombo, Store, StoreReview)


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id]


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.id]


class ContactInfoAdmin(ModelView, model=ContactInfo):
    column_list = [ContactInfo.id, ContactInfo.contact_info]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name]


class ProductComboAdmin(ModelView, model=ProductCombo):
    column_list = [ProductCombo.id, ProductCombo.combo_name]


class CourierAdmin(ModelView, model=Courier):
    column_list = [Courier.id]


class CourierReviewAdmin(ModelView, model=CourierReview):
    column_list = [CourierReview.id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id]


class StoreReviewAdmin(ModelView, model=StoreReview):
    column_list = [StoreReview.id]


class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.store_name]


