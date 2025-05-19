from django.db import models
from inventory.models import InventoryItem

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_name} ({self.start_date} - {self.end_date})"  # type: ignore[attr-defined]

class AssignedItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ("booking", "inventory_item")

    def __str__(self):
        return f"{self.inventory_item} -> {self.booking.event_name}"
