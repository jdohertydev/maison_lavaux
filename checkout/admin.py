from django.contrib import admin
from django.db.models import Sum
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('product', 'product_size', 'quantity', 'lineitem_total')


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid')

    fields = ('order_number', 'date', 'full_name', 'email', 'phone_number', 
              'country', 'postcode', 'town_or_city', 'street_address1', 
              'street_address2', 'county', 'delivery_cost', 'order_total', 'grand_total', 'original_bag',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name', 'total_items', 
                    'order_total', 'delivery_cost', 'grand_total')

    search_fields = ('order_number', 'full_name', 'email', 'phone_number')
    list_filter = ('date', 'country', 'grand_total')
    ordering = ('-date', 'order_number')

    def total_items(self, obj):
        """Returns the total quantity of items in an order."""
        return obj.lineitems.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_items.short_description = 'Total Items'

    def formatted_grand_total(self, obj):
        """Formats the grand total as currency."""
        return f"${obj.grand_total:,.2f}"
    formatted_grand_total.short_description = 'Grand Total'


admin.site.register(Order, OrderAdmin)
