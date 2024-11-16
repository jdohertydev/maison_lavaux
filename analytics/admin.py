from django.contrib import admin
from .models import SalesData


class RevenueFilter(admin.SimpleListFilter):
    title = 'Revenue Range'
    parameter_name = 'revenue_range'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Low (< $500)'),
            ('medium', 'Medium ($500-$2000)'),
            ('high', 'High (> $2000)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(revenue_generated__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(revenue_generated__gte=500, revenue_generated__lte=2000)
        elif self.value() == 'high':
            return queryset.filter(revenue_generated__gt=2000)
        return queryset


class SalesDataAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'views', 'purchases', 'added_to_cart',
        'revenue_generated', 'highlight_status', 'updated_at'
    )
    list_filter = ('updated_at', RevenueFilter)
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
