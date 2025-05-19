from django.contrib import admin
from .models import Client, Booking, AssignedItem

admin.site.register(Client)
admin.site.register(Booking)
admin.site.register(AssignedItem)
