from django.shortcuts import render
from products.models import Product
import random
from django.db.models import Count
from analytics.models import SalesData  # Correctly import SalesData model from analytics app

def home(request):
    """ A view to display homepage with various product sections """

    # New In Section (last 30 days)
    new_in_products = Product.objects.filter(created_at__gte='2024-10-18', is_active=True).order_by('-created_at')[:4]

    # For Him Section (products for men)
    for_him_products = Product.objects.filter(gender='M', is_active=True).order_by('-created_at')[:4]

    # For Her Section (products for women)
    for_her_products = Product.objects.filter(gender='W', is_active=True).order_by('-created_at')[:4]

    # Most Popular Section (based on views or sales)
    # Annotate products with the total views from the SalesData model
    most_popular_products = Product.objects.annotate(
        views_count=Count('sales_data__views')
    ).order_by('-views_count')[:4]

    # Highest Rated Section (products with the highest ratings)
    highest_rated_products = Product.objects.filter(rating__isnull=False, is_active=True).order_by('-rating')[:4]

    # Pot Luck (Random selection of 4 products)
    all_active_products = Product.objects.filter(is_active=True)
    random_products = random.sample(list(all_active_products), 4) if all_active_products else []

    # Pass all products to the context
    context = {
        'new_in_products': new_in_products,
        'for_him_products': for_him_products,
        'for_her_products': for_her_products,
        'most_popular_products': most_popular_products,
        'highest_rated_products': highest_rated_products,
        'random_products': random_products,
    }

    return render(request, 'home/index.html', context)
