from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def total_price(self):
        return self.product.price * self.quantity

image = models.ImageField(upload_to='product_images/')
