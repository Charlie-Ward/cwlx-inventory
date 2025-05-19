from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, InventoryItem, Category
from .forms import ProductForm, InventoryItemForm, CategoryForm

def item_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'inventory/item_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/add_category.html', {'form': form})

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'query': query,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    items = InventoryItem.objects.filter(product=product)
    form = InventoryItemForm(initial={'product': product})

    if request.method == "POST":
        if "add_item" in request.POST:
            form = InventoryItemForm(request.POST)
            if form.is_valid():
                new_item = form.save(commit=False)
                new_item.product = product  # Force the product
                new_item.save()
                return redirect('inventory:product_detail', pk=product.pk)
            # If not valid, fall through and render with bound form (shows errors)
        elif "toggle_available" in request.POST:
            item_id = request.POST.get("item_id")
            item = get_object_or_404(InventoryItem, pk=item_id, product=product)
            item.is_available = not item.is_available
            item.save()
            return redirect('inventory:product_detail', pk=product.pk)
        elif "delete_item" in request.POST:
            item_id = request.POST.get("item_id")
            item = get_object_or_404(InventoryItem, pk=item_id, product=product)
            item.delete()
            return redirect('inventory:product_detail', pk=product.pk)
    # If GET or invalid POST, form will be either unbound or bound with errors
    return render(request, 'inventory/product_detail.html', {
        'product': product,
        'items': items,
        'item_form': form,
    })

# Category is a preset choices enum, so you likely don't need an add_category view.
# If you want a page explaining categories, you can create a static template for that.
