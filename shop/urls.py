from django.urls import path
from .views import ShopView, CartView, CheckoutView, EmptyCart, ProductDetailsView, UpdateItemView, LogInView, \
    LogOutView

urlpatterns = [
    path('', ShopView.as_view(), name='store'),
    path('cart', CartView.as_view(), name='cart'),
    path('empty_cart', EmptyCart.as_view(), name='empty_cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('view/<str:name>', ProductDetailsView.as_view(), name='product_details'),
    path('update_item', UpdateItemView.as_view(), name='update_item'),
    path('login', LogInView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),

]
