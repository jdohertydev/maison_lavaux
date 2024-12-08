from django.shortcuts import render
from products.models import Product
from django.utils.timezone import now, timedelta
from django.db.models import Sum
import random


def home(request):
    """A view to display homepage with various product sections"""

    # Always get the 4 most recently added active products
    new_in_products = Product.objects.filter(is_active=True).order_by("-created_at")[:4]

    # For Him Section (products for men)
    for_him_products = Product.objects.filter(
        gender="M", is_active=True
    ).order_by("-created_at")[:4]

    # For Her Section (products for women)
    for_her_products = Product.objects.filter(
        gender="W", is_active=True
    ).order_by("-created_at")[:4]

    # Get top 4 products by revenue generated
    most_popular_products = Product.objects.annotate(
        total_revenue=Sum("sales_data__revenue_generated")
    ).order_by("-total_revenue")[:4]

    # Highest Rated Section (products with the highest ratings)
    highest_rated_products = Product.objects.filter(
        rating__isnull=False, is_active=True
    ).order_by("-rating")[:4]

    # Pot Luck (Random selection of 4 products)
    all_active_products = Product.objects.filter(is_active=True)
    random_products = (
        random.sample(list(all_active_products), 4)
        if all_active_products
        else []
    )

    # Meta description for SEO
    meta_description = (
        "Welcome to Maison Lavaux, your destination for handcrafted perfumes "
        "made in Paris. Explore our exclusive collection for men and women, "
        "featuring new arrivals, top-rated scents, and unique fragrances for "
        "every occasion."
    )

    # Pass all products and meta description to the context
    context = {
        "new_in_products": new_in_products,
        "for_him_products": for_him_products,
        "for_her_products": for_her_products,
        "most_popular_products": most_popular_products,
        "highest_rated_products": highest_rated_products,
        "random_products": random_products,
        "meta_description": meta_description,
    }

    return render(request, "home/index.html", context)
