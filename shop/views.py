import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView
from django.http import JsonResponse

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
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['products'] = Cart.objects.all()
            purchase, created = Purchase.objects.get_or_create(**kwargs)
            context['purchase'] = purchase
            context['is_authenticated'] = True
        else:
            return HttpResponseRedirect('empty_cart')
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


class EmptyCart(TemplateView):
    template_name = 'store/empty_cart.html'


class ProductDetailsView(TemplateView):
    template_name = 'store/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_details'] = Product.objects.all()
        return context


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product: ', product_id)

    customer = request.user.pk
    product = Product.objects.get(id=product_id)
    purchase, created = Purchase.objects.get_or_create(customer=customer)
    cart, created = Cart.objects.get_or_create(purchase=purchase, product=product)

    if action == 'add':
        cart.amount = cart.amount + 1
    elif action == 'remove':
        cart.amount = cart.amount - 1

    cart.save()

    if cart.amount <= 0:
        cart.delete()

    return JsonResponse('Item was added', safe=False)

