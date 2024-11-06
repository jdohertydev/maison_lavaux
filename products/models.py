from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex'),
    ]

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')  # Gender field
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Discounted price, if any
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)  # Track stock quantity for inventory management
    is_active = models.BooleanField(default=True)  # Indicates if the product is active
    size = models.CharField(max_length=50, null=True, blank=True)  # Perfume measurement size    
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product is created
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp for last modification

    def clean(self):
        """
        Ensure that discount_price is valid (less than price).
        """
        super().clean()
        if self.discount_price and self.discount_price >= self.price:
            raise ValidationError("Discount price must be less than the original price.")

    def __str__(self):
        return self.name