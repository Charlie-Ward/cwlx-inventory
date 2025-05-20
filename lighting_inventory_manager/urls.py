from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from bookings import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),  # Your inventory app URLs
    path('bookings/', include('bookings.urls')),
    path('', views.home, name='home'),  # Root URL for home page
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
