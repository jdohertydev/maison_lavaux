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

Pricing and Discount Logic Implementation

To enhance the shopping bag functionality, we implemented a system to dynamically handle both regular and discounted product prices. Here’s a summary of what we did:

    Dynamic Price Calculation:
        Updated the bag_contents function to determine an effective_price for each product, prioritizing the discount_price if available, and falling back to the regular price otherwise.
        Calculated the subtotal for each item based on its quantity and effective_price.

    Template Adjustments:
        Updated the shopping bag template to display the effective_price for each product and the calculated subtotal dynamically.
        Ensured that the totals and subtotals were formatted correctly and reflected discounts when applicable.

    Validation Logic:
        Ensured that the discount_price field in the database is always less than the price to maintain data integrity.

    User Experience:
        Provided dynamic updates in the bag to reflect accurate pricing, ensuring customers see discounts applied correctly.

This implementation ensures accuracy and clarity in the pricing displayed to customers, enhancing the overall user experience.

Handling Perrume Sizes in the Shopping Bag

The shopping bag functionality includes a robust solution for handling products with size variations. By dynamically checking whether a product has a size attribute before attempting to use it, the implementation prevents errors when sizes are not applicable. This approach ensures:

    Flexibility for Different Product Types: The code accommodates both products with sizes (e.g., clothing or shoes) and those without sizes (e.g., accessories or generic items), making it versatile for diverse product catalogs.
    Error Prevention: By using item_data.get('size') to check for size information in the session data, the implementation avoids the NameError issue when a size is not provided or required.
    User-Friendly Experience: Users can add products to their bag seamlessly, whether the products include size options or not, ensuring a smoother shopping experience.

This dynamic handling of size data ensures the shopping bag logic remains error-free, adaptable, and capable of supporting a wide range of product configurations.

Quanity input script

This JavaScript snippet provides dynamic management of product quantity inputs in the shopping bag. It ensures a smooth and user-friendly experience by:

    Range Enforcement:
        Prevents the quantity from going below 1 or above 99 by disabling the - (decrement) and + (increment) buttons when the limits are reached.

    Page Load Handling:
        Automatically checks and adjusts the state of the - and + buttons for all quantity inputs when the page loads.

    Dynamic Updates:
        Listens for changes in quantity inputs and updates the state of the - and + buttons accordingly.

    Increment and Decrement Controls:
        Allows users to increment or decrement the quantity using buttons. The current value is updated dynamically in the input field, and button states are adjusted.

Why This is Useful

This script enhances usability by preventing invalid quantities and provides immediate feedback through button state changes. It improves the shopping experience by making quantity adjustments seamless and intuitive.

Approach to Subtotal Calculation

In this project, the subtotal for each item in the shopping bag is calculated in the context.py file rather than using a custom Django template filter, as some implementations suggest. This decision was made for the following reasons:

    Centralized Business Logic: Calculating the subtotal in context.py keeps all shopping bag-related logic in one place, making the codebase more maintainable and easier to debug.

    Simpler Templates: By precomputing the subtotal, the templates only need to display the values passed in the context. This avoids adding unnecessary logic or filters to the templates, adhering to Django's philosophy of keeping templates simple and focused on presentation.

    Efficiency: Computing the subtotal in the context avoids redundant calculations in the template rendering process, ensuring the application runs more efficiently, especially for large bags or complex templates.

    Flexibility: Passing precomputed values like subtotal to the context allows for easier customization in the future, such as adding taxes, discounts, or other price adjustments.

This approach reflects a clean separation of concerns between business logic and presentation, ensuring the project remains scalable and maintainable.

Issue: Toast Messages Displayed Incorrect Information

Issue: Toast Messages Displayed Incorrect Information

In the initial implementation, toast messages displayed incorrect or unclear information when users added, updated, or removed items from the shopping bag. Specifically, the messages referenced raw data from the session (e.g., item IDs or quantities) instead of meaningful details like the product's name. This caused confusion for users as they were shown numbers instead of the actual product names.
Fix: Improved Toast Messaging

The messages framework was updated to dynamically include the product's name and relevant details (e.g., size and quantity) in all user feedback. This involved:

    Fetching the product name from the database (Product.objects.get(pk=item_id)).
    Updating success and warning messages to use clear, user-friendly text.
    Including size and quantity details where applicable for better context.

This fix ensures that all toast messages provide accurate and meaningful feedback, enhancing the user experience. For example:

    Before: Updated quantity to 2.
    After: Updated 'Product Name' quantity to 2.

Relevant Files

    views.py: Adjusted logic for add_to_bag, adjust_bag, and remove_from_bag to include meaningful details in toast messages.

Admin Panel Enhancements for the Checkout App

We improved the admin.py file for the checkout app to enhance the usability and efficiency of the admin interface. Here’s a summary of the improvements:
Original Code:

    The initial implementation included basic inline editing for OrderLineItem and read-only fields for Order totals, such as order_total and grand_total.
    While functional, it lacked features like search, filtering, and formatted display of key information, making order management less efficient.

Improvements:

    Search Functionality:
        Added the search_fields attribute to enable admins to search orders by key attributes such as:
            order_number
            full_name
            email
            phone_number

    Benefit: Speeds up locating specific orders in the admin panel.

search_fields = ('order_number', 'full_name', 'email', 'phone_number')

Filtering Options:

    Introduced list_filter to filter orders by:
        date
        country
        grand_total

Benefit: Helps admins quickly narrow down orders based on criteria like date or order value.

list_filter = ('date', 'country', 'grand_total')

Improved Display of Totals:

    Created a custom method formatted_grand_total to format grand_total as currency for better readability.

Benefit: Admins can now see monetary totals in a user-friendly format.

def formatted_grand_total(self, obj):
    return f"${obj.grand_total:,.2f}"
formatted_grand_total.short_description = 'Grand Total'

Aggregate Total Items:

    Added the total_items method to display the total quantity of items in an order.

Benefit: Admins can easily see how many items were purchased in each order without opening individual line items.

def total_items(self, obj):
    return obj.lineitems.aggregate(Sum('quantity'))['quantity__sum'] or 0
total_items.short_description = 'Total Items'

Enhanced Inline Editing:

    Improved the OrderLineItemAdminInline to show:
        product
        product_size
        quantity
        lineitem_total

Benefit: Provides more context for line items directly in the order view.

readonly_fields = ('product', 'product_size', 'quantity', 'lineitem_total')

Ordering Improvements:

    Updated the ordering attribute to sort by:
        date (descending)
        order_number (secondary sorting)

Benefit: Maintains a logical order for viewing recent orders while ensuring consistency.

    ordering = ('-date', 'order_number')

Final Code:

The final implementation is a more user-friendly and efficient admin panel that supports:

    Search functionality
    Filtering by key attributes
    Aggregated and formatted totals
    Enhanced inline editing for order line items

These changes improve admin productivity and simplify the management of orders in the application.

mprovements to the Checkout Form

The original OrderForm provided basic functionality for capturing user data during the checkout process. We made several enhancements to improve usability, accessibility, and data validation. Here’s an overview of the improvements:
Original Code:

    Dynamically set placeholders for each field.
    Added CSS classes for consistent styling with Stripe.
    Hid labels for a cleaner design.
    Automatically focused on the full_name field.

Improvements Made:

    Improved Field Accessibility:
        Explicitly defined input types for email and phone_number fields to enhance usability and improve validation in the browser.

    self.fields['email'].widget.attrs['type'] = 'email'
    self.fields['phone_number'].widget.attrs['type'] = 'tel'

Benefit: This helps users enter valid data and ensures fields are tailored for their purpose, improving the overall user experience.

Enhanced Placeholder Management:

    Kept the dynamic placeholders but ensured consistency for required fields by appending an asterisk (*).

    if self.fields[field].required:
        placeholder = f'{placeholders[field]} *'

Benefit: This visually indicates required fields without relying on labels.

Optional Country Field Improvements:

    Suggested enhancements for the country field to either:
        Use django-countries for pre-defined country choices.
        Or, explicitly define dropdown options using a ChoiceField.

Benefit: This ensures that the country field is more structured and user-friendly.

Maintained Autofocus on the First Field:

    Retained autofocus for the full_name field, ensuring that users are immediately directed to start entering their information.

Benefit: Streamlines the checkout process and minimizes user effort.

Validation Suggestions:

    Recommended adding validation for specific fields, such as checking for numeric-only phone numbers:

        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if not phone_number.isdigit():
                raise forms.ValidationError('Phone number must contain only digits.')
            return phone_number

    Benefit: Helps maintain clean and valid data in the database.

    Code Readability and Maintainability:
        Cleaned up the code for easier understanding and maintenance. For example, grouped enhancements logically and added comments for clarity.

Final Outcome:

The improved OrderForm is more robust, user-friendly, and accessible. These enhancements:

    Improve the user experience by guiding users with appropriate input types and placeholders.
    Support accessibility and responsiveness by hiding labels while ensuring fields remain intuitive.
    Provide a foundation for future improvements, such as dropdowns for countries or advanced validation rules.

Issue with JavaScript and Why CSS Was Used

Initially, JavaScript was implemented to manage custom increment and decrement buttons for quantity input fields. While it successfully controlled these buttons and enforced value limits, it did not disable or hide the browser's default spinner arrows for type="number" input fields. These spinner arrows are a built-in feature of modern browsers and are not directly addressed by JavaScript without additional logic, such as altering the input type or blocking arrow key events. However, such approaches add complexity and may lead to inconsistent behavior across different browsers.

To resolve this, CSS was used to hide the spinner arrows. This solution is simpler, cleaner, and more reliable, as it directly targets the browser-specific pseudo-elements responsible for rendering the spinners. By using CSS, the UI was streamlined without compromising functionality, allowing the custom buttons to handle all user interactions seamlessly.


{% if grand_total and not on_profile_page %} profile app p6