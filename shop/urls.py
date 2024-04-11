from django.urls import path
from .views import ShopView, CartView, CheckoutView

urlpatterns = [
    path('', ShopView.as_view(), name='store'),
    path('cart', CartView.as_view(), name='cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),

]
