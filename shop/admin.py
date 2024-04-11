from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'producer',
        'material',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(Cart)
