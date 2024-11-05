from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'discount_price',
        'stock_quantity',
        'is_active',
        'size',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('category', 'is_active')  # Filter options for category and active status
    search_fields = ('name', 'sku')  # Enable search by name and SKU
    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
