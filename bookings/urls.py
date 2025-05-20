from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('', views.booking_list, name='list'),
    path('manage/<int:booking_id>/', views.manage_booking, name='manage_booking'),
    path('available-items/', views.available_items_api, name='available_items_api'),
    path('clients/', views.manage_clients, name='manage_clients'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/edit/', views.edit_client, name='edit_client'),
    path('clients/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    path('bookings/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('clients/add/', views.add_client, name='add_client'),
]
