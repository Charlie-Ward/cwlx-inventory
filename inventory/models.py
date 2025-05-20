from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    barcode = models.CharField(max_length=100, unique=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)  # <-- Add this line

    def __str__(self):
        return f"{self.product.name} - {self.barcode}"

