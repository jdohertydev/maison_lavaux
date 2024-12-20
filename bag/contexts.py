from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Generates the shopping bag contents, including items, totals,
    delivery costs, and grand total for the current session.
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if isinstance(item_data, dict):
            quantity = item_data["quantity"]
            size = item_data.get("size", None)
        else:
            quantity = item_data
            size = None

        price = (
            product.discount_price if product.discount_price else product.price
        )
        subtotal = quantity * price
        total += subtotal
        product_count += quantity
        bag_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
                "size": size,
                "effective_price": price,
                "subtotal": subtotal,
            }
        )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
