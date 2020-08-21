from django.contrib import admin

# Register your models here.
from .models import Customer, Product, Order, Category

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
