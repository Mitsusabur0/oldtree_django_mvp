# stock_api/admin.py

from django.contrib import admin
from .models import Product, ProductVariant, Location, StockLevel, StockMovement

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Location)
admin.site.register(StockLevel)
admin.site.register(StockMovement)