from django.contrib import admin
from .models import Product, InventoryItem

admin.site.register(Product)
admin.site.register(InventoryItem)