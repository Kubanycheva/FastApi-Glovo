from sqladmin import Admin, ModelView
from models import (UserProfile, Category, Store, ContactInfo, Product, ProductCombo,
                    Cart, CartItem, StoreReview, CourierReview, Order, Courier)
from database import engine


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]
    name = 'User'
    name_plural = 'Users'


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    name = 'Category'
    name_plural = 'Categories'


class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.store_name]
    name = 'Store'
    name_plural = 'Stores'


class ContactInfoAdmin(ModelView, model=ContactInfo):
    column_list = [ContactInfo.id, ContactInfo.contact_info]
    name = 'ContactInfo'
    name_plural = 'ContactInfos'


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name]
    name = 'Product'
    name_plural = 'Products'


class ProductComboAdmin(ModelView, model=ProductCombo):
    column_list = [ProductCombo.id, ProductCombo.combo_name]
    name = 'ProductCombo'
    name_plural = 'ProductCombo'


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id]
    name = 'Cart'
    name_plural = 'Carts'


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.id, CartItem.quantity]
    name = 'CartItem'
    name_plural = 'CartItems'


class StoreReviewAdmin(ModelView, model=StoreReview):
    column_list = [StoreReview.id, StoreReview.created_date]
    name = 'StoreReview'
    name_plural = 'StoreReviews'


class CourierReviewAdmin(ModelView, model=CourierReview):
    column_list = [CourierReview.id, CourierReview.rating]
    name = 'CourierReview'
    name_plural = 'CourierReviews'


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.status]
    name = 'Order'
    name_plural = 'Orders'


class CourierAdmin(ModelView, model=Courier):
    column_list = [Courier.id, Courier.type]
    name = 'Courier'
    name_plural = 'Couriers'


def create_admin(app):
    admin = Admin(app, engine)

    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ContactInfoAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductComboAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)
    admin.add_view(StoreReviewAdmin)
    admin.add_view(CourierReviewAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(CourierAdmin)

    return admin