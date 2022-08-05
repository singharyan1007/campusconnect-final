from django.contrib import admin

# Register your models here.
from.models import Product, Order, Address
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)



