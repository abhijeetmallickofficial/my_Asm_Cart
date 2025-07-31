
from django.contrib import admin
from .models import Product, Order, OrderUpdate
from .models import Contact

# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)

