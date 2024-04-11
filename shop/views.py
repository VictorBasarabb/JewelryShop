from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import *


class ShopView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Cart.objects.all()
        purchase, created = Purchase.objects.get_or_create(**kwargs)
        context['purchase'] = purchase
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    # TODO: implement not authenticated user cart


class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Cart.objects.all()
        purchase, created = Purchase.objects.get_or_create(**kwargs)
        context['purchase'] = purchase
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


