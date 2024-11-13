from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 0))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size', None)
    bag = request.session.get('bag', {})

    # Validate stock availability
    if quantity > product.stock_quantity:
        messages.error(
            request, f"Sorry, only {product.stock_quantity} of '{product.name}' are available."
        )
        return redirect(redirect_url)

    if size:
        if item_id in bag:
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size] += quantity
                if bag[item_id]['items_by_size'][size] > product.stock_quantity:
                    messages.error(
                        request, f"Sorry, only {product.stock_quantity} of '{product.name}' in size {size.upper()} are available."
                    )
                    bag[item_id]['items_by_size'][size] -= quantity
                    return redirect(redirect_url)
                messages.success(
                    request, f"Updated size {size.upper()} '{product.name}' quantity to {bag[item_id]['items_by_size'][size]}."
                )
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f"Added size {size.upper()} '{product.name}' to your bag.")
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f"Added size {size.upper()} '{product.name}' to your bag.")
    else:
        if item_id in bag:
            bag[item_id] += quantity
            if bag[item_id] > product.stock_quantity:
                messages.error(
                    request, f"Sorry, only {product.stock_quantity} of '{product.name}' are available."
                )
                bag[item_id] -= quantity
                return redirect(redirect_url)
            messages.success(request, f"Updated '{product.name}' quantity to {bag[item_id]}.")
        else:
            bag[item_id] = quantity
            messages.success(request, f"Added '{product.name}' to your bag.")

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 0))
    size = request.POST.get('product_size', None)
    bag = request.session.get('bag', {})

    # Validate stock availability
    if quantity > product.stock_quantity:
        messages.error(
            request, f"Sorry, only {product.stock_quantity} of '{product.name}' are available."
        )
        return redirect(reverse('view_bag'))

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f"Updated size {size.upper()} '{product.name}' quantity to {quantity}.")
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.warning(request, f"Removed size {size.upper()} '{product.name}' from your bag.")
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f"Updated '{product.name}' quantity to {quantity}.")
        else:
            bag.pop(item_id)
            messages.warning(request, f"Removed '{product.name}' from your bag.")

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size', None)
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.warning(request, f"Removed size {size.upper()} '{product.name}' from your bag.")
        else:
            bag.pop(item_id)
            messages.warning(request, f"Removed '{product.name}' from your bag.")

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
