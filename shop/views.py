import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from django.http import JsonResponse

from .models import *


class ShopView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        customer = self.request.user.pk
        purchase, created = Purchase.objects.get_or_create(customer=customer)
        cart_items = purchase.get_cart_products
        context['cart_items'] = cart_items
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):

        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['products'] = Cart.objects.all()
            purchase, created = Purchase.objects.get_or_create(customer=self.request.user.pk)
            context['purchase'] = purchase
            # customer = self.request.user.pk
            # purchase, created = Purchase.objects.get_or_create(customer=customer)
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
        customer = self.request.user.pk
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
        customer = self.request.user.pk
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


class LogInView(TemplateView):
    template_name = 'store/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("store"))
        context = self.get_context_data()
        context['error'] = 'Invalid Parameters!'
        context['username'] = username
        return self.render_to_response(context=context)


class LogOutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request=request)
        return HttpResponseRedirect(reverse("login"))


# class SignUpView(TemplateView):
#     template_name = 'store/signup.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['signup_form'] = UserCreationForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         print(request.POST)
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             login(request, user=form.instance)
#             return HttpResponseRedirect(reverse("store"))
#         context = self.get_context_data()
#         context['signup_form'] = form
#         return self.render_to_response(context=context)


class ProductListViewByCategory(ListView):
    template_name = 'store/products_by_category.html'
    context_object_name = 'filtred_products'
    model = Product

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Product.objects.filter(category__name=category_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.pk
        purchase, created = Purchase.objects.get_or_create(customer=customer)
        cart_items = purchase.get_cart_products
        context['cart_items'] = cart_items
        return context
