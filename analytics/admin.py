from django.contrib import admin
from .models import SalesData

class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'views', 'purchases', 'added_to_cart', 'revenue_generated', 'highlight_status', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('product__name',)
    ordering = ('-views',)

    def highlight_status(self, obj):
        """Highlight top-selling or trending products."""
        if obj.purchases >= 10:  # Example threshold for top products
            return "🔥 Top Seller"
        elif obj.views >= 50:
            return "⭐ Trending"
        return "Regular"
    highlight_status.short_description = "Status"

admin.site.register(SalesData, SalesDataAdmin)
