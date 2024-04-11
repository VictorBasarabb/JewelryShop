from django.urls import path
from .views import ShopView, CartView, CheckoutView, EmptyCart

urlpatterns = [
    path('', ShopView.as_view(), name='store'),
    path('cart', CartView.as_view(), name='cart'),
    path('empty_cart', EmptyCart.as_view(), name='empty_cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),

]
