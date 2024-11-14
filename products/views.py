from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Case, When, F, Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from .forms import ReviewForm

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Annotate products with effective_price
    products = Product.objects.all().annotate(
        effective_price=Case(
            When(discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
        )
    )

    query = None
    categories = None
    sortkey = None
    direction = None

    # Handle sorting
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'name':
                products = products.annotate(lower_name=Lower('name'))
                sortkey = 'lower_name'
            elif sortkey == 'price':
                sortkey = 'effective_price'
            elif sortkey == 'category':
                sortkey = 'category__name'
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            
            products = products.order_by(sortkey)

        # Handle category filtering
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Handle search queries
        if 'q' in request.GET:
            query = request.GET['q']
            if not query.strip():
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Context for the template
    current_sorting = f'{sortkey}_{direction}' if sortkey else 'None_None'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details and reviews """

    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()

    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request, product_id):
    """Add a new review for a product."""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Assuming user authentication is in place
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'products/add_review.html', context)

@login_required
def edit_review(request, product_id, review_id):
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(Review, pk=review_id, product=product, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'product': product,
        'review': review,
    }
    return render(request, 'products/edit_review.html', context)

@login_required
def delete_review(request, product_id, review_id):
    """Delete a specific review."""
    review = get_object_or_404(Review, pk=review_id, product_id=product_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('product_detail', product_id=product_id)

    return render(request, 'products/confirm_delete_review.html', {
        'review': review,
        'product': review.product,
    })
