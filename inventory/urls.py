from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('product/<int:product_pk>/add-item/', views.add_inventory_item, name='add_inventory_item'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('item/<int:pk>/edit/', views.edit_inventory_item, name='edit_inventory_item'),
    path('item/<int:item_id>/barcode/', views.download_barcode, name='download_barcode'),
]
