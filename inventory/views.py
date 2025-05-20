from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, InventoryItem, Category
from .forms import ProductForm, InventoryItemForm, CategoryForm
import io
from django.http import HttpResponse, JsonResponse
import barcode
from barcode.writer import ImageWriter

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
    category_id = request.GET.get('category', '')
    products = Product.objects.all()
    categories = Category.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    search_query = request.GET.get('barcode', '')
    items = InventoryItem.objects.filter(product=product)
    if search_query:
        items = items.filter(barcode__icontains=search_query)
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
        'search_query': search_query,
    })

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('inventory:product_list')
    return redirect('inventory:product_list')

def add_inventory_item(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.product = product  # Ensure correct product
            new_item.save()
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_inventory_item.html', {
        'form': form,
        'product': product,
    })

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_product.html', {
        'form': form,
        'product': product,
    })

def edit_inventory_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_detail', pk=item.product.pk)
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/edit_inventory_item.html', {
        'form': form,
        'item': item,
    })

def download_barcode(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    barcode_value = item.barcode
    barcode_format = barcode.get_barcode_class('code128')
    buffer = io.BytesIO()
    barcode_format(barcode_value, writer=ImageWriter()).write(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename=barcode_{barcode_value}.png'
    return response

def scan_barcode(request):
    error = None
    if request.method == "POST":
        barcode = request.POST.get("barcode")
        try:
            item = InventoryItem.objects.get(barcode=barcode)
            return redirect('inventory:edit_inventory_item', pk=item.pk)
        except InventoryItem.DoesNotExist:
            error = "No item found with that barcode."
    return render(request, "inventory/scan_barcode.html", {"error": error})

def next_barcode(request):
    last_item = InventoryItem.objects.order_by('-barcode').first()
    if last_item and last_item.barcode.isdigit():
        next_number = int(last_item.barcode) + 1
    else:
        next_number = 1
    next_barcode = str(next_number).zfill(12)
    return JsonResponse({'barcode': next_barcode})
