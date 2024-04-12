import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    producer = models.CharField(max_length=64, null=True)
    material = models.CharField(max_length=64, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    size_in_stock = ArrayField(models.IntegerField(), blank=True, null=True)
    size_available_to_order = ArrayField(models.IntegerField(), blank=True)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    description = models.TextField(null=True, blank=True)
    code = models.DecimalField(max_digits=15, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    # @property
    def image_URL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=64, null=True)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    date = models.DateField(auto_now_add=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        cart = self.cart_set.all()
        total = sum([product.get_total_price() for product in cart])
        return total

    @property
    def get_cart_products(self):
        cart = self.cart_set.all()
        total = sum([product.amount for product in cart])
        return total


class Cart(models.Model):
    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def get_total_price(self):
        total_price = self.product.price * self.amount
        return total_price
