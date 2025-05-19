from django import forms
from .models import Product, InventoryItem, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description']

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['product', 'barcode', 'serial_number', 'is_available']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']