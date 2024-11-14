from django.contrib import admin
from .models import Product, Category, Review


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
        'rating',  # Display rating here
        'gender',
        'created_at',
        'updated_at',
    )
    list_filter = ('category', 'is_active', 'gender')  # Filter options for category and active status
    search_fields = ('name', 'sku')  # Enable search by name and SKU
    ordering = ('sku',)
    readonly_fields = ('rating',)  # Make rating visible but read-only in the detail view



class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'rating',
        'comment',
        'created_at',
        'updated_at',
    )
    list_filter = ('product', 'rating')  # Filter by product and rating
    search_fields = ('product__name', 'user__username', 'comment')  # Search by product name, username, and comment
    ordering = ('-created_at',)  # Order by the newest reviews first


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
