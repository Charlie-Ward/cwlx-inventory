from django.shortcuts import render
from .models import Product, InventoryItem, Category

def item_list(request):
    category = request.GET.get('category')
    products = Product.objects.all()
    if category in Category.values:
        products = products.filter(category=category)
    return render(request, 'inventory/item_list.html', {
        'products': products,
        'categories': Category.choices,
        'selected_category': category,
    })
