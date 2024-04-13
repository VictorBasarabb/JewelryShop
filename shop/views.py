import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, UpdateView, DetailView
from django.http import JsonResponse

from .models import *


class ShopView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        customer = self.request.user.customer
        purchase, created = Purchase.objects.get_or_create(customer=customer)
        cart_items = purchase.get_cart_products
        context['cart_items'] = cart_items
        return context


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):

        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['products'] = Cart.objects.all()
            purchase, created = Purchase.objects.get_or_create(**kwargs)
            context['purchase'] = purchase
            customer = self.request.user.customer
            purchase, created = Purchase.objects.get_or_create(customer=customer)
            cart_items = purchase.get_cart_products
            context['cart_items'] = cart_items
            context['is_authenticated'] = True
        else:
            return HttpResponseRedirect('empty_cart')
        return context


class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Cart.objects.all()
        purchase, created = Purchase.objects.get_or_create(**kwargs)
        context['purchase'] = purchase
        context['is_authenticated'] = self.request.user.is_authenticated
        customer = self.request.user.customer
        purchase, created = Purchase.objects.get_or_create(customer=customer)
        cart_items = purchase.get_cart_products
        context['cart_items'] = cart_items
        return context


class EmptyCart(TemplateView):
    template_name = 'store/empty_cart.html'


class ProductDetailsView(DetailView):
    template_name = 'store/product_details.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        purchase, created = Purchase.objects.get_or_create(customer=customer)
        cart_items = purchase.get_cart_products
        context['cart_items'] = cart_items
        return context

    def get_object(self, queryset=None):
        return self.model.objects.get(name=self.kwargs.get('name'))


class UpdateItemView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        print('Action: ', action)
        print('Product: ', product_id)

        customer = request.user.customer
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

# def update_item(request):
#     data = json.loads(request.body)
#     product_id = data['productId']
#     action = data['action']
#     print('Action: ', action)
#     print('Product: ', product_id)
#
#     customer = request.user.customer
#     product = Product.objects.get(id=product_id)
#     purchase, created = Purchase.objects.get_or_create(customer=customer)
#     cart, created = Cart.objects.get_or_create(purchase=purchase, product=product)
#
#     if action == 'add':
#         cart.amount = cart.amount + 1
#     elif action == 'remove':
#         cart.amount = cart.amount - 1
#
#     cart.save()
#
#     if cart.amount <= 0:
#         cart.delete()
#
#     return JsonResponse('Item was added', safe=False)

