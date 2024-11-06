Running notes

Customise admin to make it more user friendly

list_filter: Adding filters for category and is_active allows you to quickly narrow down products by their category or active status.
search_fields: Adding search_fields for name and sku enables quick searches, making it easier to locate specific products.
ordering: Keeping the ordering by SKU or any other relevant field provides consistency in the display order.

Discount price 

    Conditionally Displayed Prices:
        If product.discount_price exists, the original product.price is displayed with a strikethrough (text-decoration: line-through;) and muted color.
        The discounted price (product.discount_price) is highlighted in a bold, different color (e.g., text-danger for red in Bootstrap).
    Fallback:
        If there’s no discount_price, only product.price is displayed normally.

Q

f request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

Summary: Implementing effective_price for Custom Sorting

To allow products to be sorted by price while prioritizing discount_price over the original price, we implemented the following steps:

    Annotated the Queryset:
        We used Django’s annotate method to dynamically create an effective_price field. This field checks if a discount_price exists for a product and uses it; otherwise, it defaults to the regular price.
        This was achieved using Case and When expressions:

    products = products.annotate(
        effective_price=Case(
            When(discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
        )
    )

Updated the Sorting Logic:

    In the all_products view, we modified the sort parameter to support effective_price. If the user selects to sort by price, the view orders the products by the annotated effective_price field, ascending or descending based on the direction parameter.

Adjusted Template Links:

    We updated the href attributes of the dropdown links in the template to use effective_price for sorting. For example:

        <a href="{% url 'products' %}?sort=effective_price&direction=asc" class="dropdown-item">By Price</a>

    Handled Sorting Directions:
        We incorporated the direction parameter to allow both ascending (asc) and descending (desc) sorting by effective_price.

    Tested Functionality:
        We verified that products with a discount_price appear in the correct order (sorted by discount_price first) and fallback to the original price when no discount_price exists.

Benefits:

    This approach ensures that discounts are prioritized during sorting, providing a better user experience for customers looking for the most relevant price.
    It is dynamic, leveraging Django’s ORM to handle complex logic without requiring changes to the database schema.

This functionality is fully integrated into the existing filtering and sorting system.

Sorting 

Sorting Functionality: This project includes a JavaScript-powered dynamic sorting feature. When a user selects an option from the sorting dropdown, the page automatically updates to reflect their choice. The script updates the URL query parameters (sort and direction) based on the selection and reloads the page with the new parameters.

This ensures a seamless and user-friendly way to filter and sort products by criteria like price, rating, or name. Additionally, the "Reset" option clears all sorting parameters and reloads the default product list.