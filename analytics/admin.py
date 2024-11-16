from django.contrib import admin
from .models import SalesData

class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'views', 'purchases', 'added_to_cart', 'revenue_generated', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('product__name',)

admin.site.register(SalesData, SalesDataAdmin)
