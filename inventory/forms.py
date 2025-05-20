from django import forms
from .models import Product, InventoryItem, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description']

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        exclude = ['product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'barcode' in self.fields:
            self.fields['barcode'].widget.attrs.update({'id': 'barcode-field'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']