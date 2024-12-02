from django.contrib import admin
from .models import SalesData
from products.models import Product
from django.db.models import F


class RevenueFilter(admin.SimpleListFilter):
    """
    Custom filter for revenue ranges in the SalesDataAdmin.
    Filters sales data by low, medium, and high revenue ranges.
    """

    title = "Revenue Range"
    parameter_name = "revenue_range"

    def lookups(self, request, model_admin):
        """Define the options for the revenue filter."""
        return [
            ("low", "Low (< $500)"),
            ("medium", "Medium ($500-$2000)"),
            ("high", "High (> $2000)"),
        ]

    def queryset(self, request, queryset):
        """Filter the queryset based on the selected revenue range."""
        if self.value() == "low":
            return queryset.filter(revenue_generated__lt=500)
        elif self.value() == "medium":
            return queryset.filter(
                revenue_generated__gte=500, revenue_generated__lte=2000
            )
        elif self.value() == "high":
            return queryset.filter(revenue_generated__gt=2000)
        return queryset


class SalesDataAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SalesData model.
    Displays key metrics such as views, purchases, and revenue.
    """

    list_display = (
        "product",
        "views",
        "purchases",
        "added_to_cart",
        "get_product_rating",
        "revenue_generated",
        "highlight_status",
        "updated_at",
    )
    list_filter = ("updated_at", RevenueFilter)
    search_fields = ("product__name",)
    ordering = ("-views",)

    def get_queryset(self, request):
        """
        Override the queryset to ensure all products appear in the admin,
        even if they don't have associated SalesData.
        Automatically creates missing SalesData entries for active products.
        """
        qs = super().get_queryset(request)
        all_products = Product.objects.filter(is_active=True)
        for product in all_products:
            SalesData.objects.get_or_create(product=product)
        return qs

    def highlight_status(self, obj):
        """
        Highlight top-selling or trending products based on thresholds.
        Returns a label for visual status representation.
        """
        if obj.purchases >= 10:  # Example threshold for top products
            return "🔥 Top Seller"
        elif obj.views >= 50:
            return "⭐ Trending"
        return "Regular"

    highlight_status.short_description = "Status"

    def get_product_rating(self, obj):
        """
        Fetch the product rating from the Product model.
        Enables sorting by the rating field in the admin interface.
        """
        return obj.product.rating

    get_product_rating.short_description = "Rating"
    get_product_rating.admin_order_field = "product__rating"


admin.site.register(SalesData, SalesDataAdmin)
