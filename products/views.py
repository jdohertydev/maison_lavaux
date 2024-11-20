from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, F, Q
from django.db.models.functions import Lower
from analytics.models import SalesData 

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm

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
    meta_description = "Browse Maison Lavaux's collection of handcrafted perfumes. Discover unique scents for men and women, including our bestsellers and new arrivals."

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
            meta_description = f"Explore our {', '.join([cat.friendly_name for cat in categories])} collection. Handcrafted luxury fragrances from Paris."

        # Handle search queries
        if 'q' in request.GET:
            query = request.GET['q']
            if not query.strip():
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
            meta_description = f"Search results for '{query}'. Discover handcrafted perfumes by Maison Lavaux."

    # Context for the template
    current_sorting = f'{sortkey}_{direction}' if sortkey else 'None_None'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'meta_description': meta_description,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details and reviews """
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()

    # Increment product views in SalesData
    sales_data, created = SalesData.objects.get_or_create(product=product)
    sales_data.views += 1
    sales_data.save()

    # Determine if the logged-in user has already reviewed this product
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()

    # Meta description
    meta_description = f"Discover {product.name} by Maison Lavaux. Handcrafted in Paris, this luxurious fragrance offers sophistication and elegance."

    context = {
        'product': product,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
        'meta_description': meta_description,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request, product_id):
    """Add a new review for a product."""
    product = get_object_or_404(Product, pk=product_id)

    # Check if the user has already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, "You have already reviewed this product.")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, "Thank you for your review!")
                return redirect('product_detail', product_id=product.id)
            except IntegrityError:
                messages.error(request, "An error occurred while saving your review.")
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

@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))