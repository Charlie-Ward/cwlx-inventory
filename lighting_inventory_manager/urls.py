from django.urls import path, include
from django.contrib import admin
from bookings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),  # Your inventory app URLs
    path('bookings/', include('bookings.urls')),
    path('', views.home, name='home'),  # Root URL for home page
]
