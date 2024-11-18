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

Pre-Filled Read-Only Fields for Logged-In Users

The contact form now includes a feature that automatically pre-fills the "Name" and "Email" fields for logged-in users. These fields are set to read-only, ensuring that user information remains consistent and cannot be altered unintentionally. This enhancement improves user experience by streamlining the form submission process while maintaining data integrity. The fields are visually greyed out to indicate they are non-editable, providing clear feedback to users.

Updates and Fixes for Stripe Webhooks (Nov 14, 2024)
Overview

This morning's work focused on refining the Stripe webhook handler to address several critical issues related to order processing, inventory management, and admin functionality. These changes ensure a smoother user experience and improve backend accuracy.
Key Issues Addressed

    Duplicate Order Line Items in Admin:
        Fixed a bug where order line items were being duplicated in the admin interface.
        Ensured that existing line items are updated instead of creating duplicates when processing orders.

    Inventory Management:
        Resolved a critical issue where stock quantities were not being reduced correctly after order creation.
        Implemented logic to accurately adjust stock levels for products, whether they are standard items or have specific sizes.

    Order Line Item Quantities:
        Updated logic to ensure the quantity of existing order line items is reset to the correct value, avoiding unintended accumulation.

    User Profile Handling:
        Improved handling of user profiles to update saved shipping information only when explicitly requested by the user.

    Logging and Debugging:
        Added detailed print statements and logging to track inventory updates and order processing in real-time, facilitating debugging and improving transparency.

Steps Taken

    Refactored _update_inventory Method:
        Centralized logic for handling product stock updates and order line item creation.
        Used get_or_create for order line items to handle both new and existing entries, updating quantities as needed.

    Improved Stock Adjustments:
        Ensured that product stock is reduced only once per order, with accurate calculations for single items and items with sizes.

    Enhanced Webhook Logic:
        Implemented robust error handling and rollback mechanisms to prevent partial orders or incorrect inventory updates.
        Ensured that emails are sent to users only after all processing steps are successful.

    Manual Testing:
        Conducted thorough manual testing to verify fixes:
            Placed orders with varying quantities.
            Confirmed correct stock adjustments.
            Checked admin interface for proper order line item behavior.

Results

    Bug-Free Admin Experience: Admins now see accurate order line items without duplication.

    Accurate Inventory Management: Product stock updates correctly reflect user purchases, ensuring inventory integrity.

    Improved User Experience: Users receive accurate order confirmations with proper details.

Future Improvements

    Unit Tests: Add automated tests for webhook handling and inventory updates to catch edge cases.
    Error Notifications: Implement email or logging notifications for critical webhook errors.
    Optimized Logging: Replace verbose logs with more structured and configurable logging.

This update ensures that the Stripe webhook handler is more reliable, scalable, and user-friendly. All fixes have been committed to the repository and tested extensively.

Review feature

Implementation Details
1. Database Structure

    Models:
        Product: Modified to calculate the average rating dynamically from associated reviews.
        Review: New model that stores product, user, rating, and comment. It includes a unique_together constraint to ensure a user can only review a product once.

2. Views

    Added views for the following operations:
        add_review: Displays a form to add a review.
        edit_review: Allows users to modify an existing review.
        delete_review: Displays a confirmation page and deletes the review upon confirmation.

3. Templates

    Created three templates:
        Add Review: Provides a user-friendly form with radio buttons for rating selection.
        Edit Review: Displays the pre-filled form for review editing.
        Delete Review: Confirmation page showing the review details before deletion.

4. Forms

    Created ReviewForm for adding and editing reviews.
    Enhanced the rating field with radio buttons for intuitive selection.

5. URL Routing

    Updated products/urls.py to include routes for:
        Adding a review: products/<product_id>/reviews/add/
        Editing a review: products/<product_id>/reviews/<review_id>/edit/
        Deleting a review: products/<product_id>/reviews/<review_id>/delete/

6. Admin Integration

    Updated the admin panel to manage reviews effectively:
        Included Review in the admin panel.
        Added inline editing of reviews under the product management interface.

7. Front-End Integration

    Updated the product detail page to include:
        A review section with:
            User reviews displayed in a styled list.
            Buttons for editing and deleting reviews for the respective user.
        A "Write a Review" button if the user hasn’t reviewed the product yet.

User Flow

    Viewing Reviews:
        Users navigate to a product detail page and see existing reviews and overall product rating.
    Adding a Review:
        If a user hasn’t reviewed the product, they can click "Write a Review," fill out the form, and submit.
    Editing a Review:
        Users click "Edit" on their review, modify the details in the pre-filled form, and save changes.
    Deleting a Review:
        Users click "Delete" on their review, confirm the deletion, and remove it permanently.

Validation and Security

    Users can only edit or delete their own reviews.
    Review input is validated to ensure the rating is within 0-5 and comments are optional but encouraged.
    CSRF tokens are implemented for all forms to prevent cross-site request forgery attacks.

Benefits of the Review Functionality

    Encourages customer engagement and feedback.
    Helps potential customers make informed purchasing decisions by reading authentic reviews.
    Provides a clear and transparent mechanism for gathering product feedback.

This feature is a robust addition to the platform, enhancing both user experience and product discoverability.

Dynamic Product Rating System

The product rating system has been enhanced to dynamically calculate and update the average rating based on user reviews. This ensures that the displayed rating is always accurate and reflects real user feedback.
Key Features:

    Real-time Updates: The product's average rating updates dynamically whenever a review is added, edited, or deleted.
    Integration with Admin Panel: The updated rating is displayed in the Django admin interface for better product management.
    Automatic Calculation: The average rating is calculated using Django signals (post_save and post_delete), ensuring seamless updates without manual intervention.

Technical Implementation:

    Signals Setup:
        A post_save signal was implemented to update the product's rating whenever a review is saved.
        A post_delete signal recalculates the rating when a review is deleted.

    Model Adjustments:
        The rating field in the Product model is marked as editable=False to enforce that it is calculated dynamically.

    App Configuration:
        The signals.py file is loaded in the ready method of the ProductsConfig class.

How It Works:

    When a review is created, updated, or deleted, the product's update_rating method is triggered via signals.
    The method calculates the average rating based on all associated reviews.
    The calculated rating is saved to the rating field in the Product model.

Benefits:

    Ensures the product rating reflects genuine user feedback in real-time.
    Reduces manual workload for administrators.
    Enhances user trust by displaying accurate product ratings.

README Update
Preventing Duplicate Reviews

This update improves the review system by ensuring that users can submit only one review per product. Duplicate reviews were previously causing database integrity errors due to unique constraints on the Review model. By adding custom validation to the ReviewForm and updating the add_review view, this fix ensures:

    A smoother user experience by informing users they have already reviewed the product.
    Robust backend validation to avoid crashes or errors if a duplicate review is attempted.
    Flexibility for users to edit their existing reviews instead of submitting multiple entries.

This enhancement improves application stability and ensures fair and clean review management for all users.

README Update: Dynamic Tab Title Feature
Dynamic Tab Titles for Improved User Engagement

The dynamic tab title feature is designed to enhance user retention and engagement by changing the browser tab's title when a user navigates away. This subtle reminder can help draw users back to your site, which is particularly valuable for e-commerce platforms where attention and retention are critical to increasing conversions.
How It Works

    Visibility Detection: The feature leverages the visibilitychange event, which detects when a browser tab becomes hidden (inactive) or visible (active).
    Title Change: When the tab is hidden, the page title changes to a predefined message (e.g., "Come back soon! 🛍️"). When the user returns to the tab, the original title is restored.

Code Implementation

The functionality is implemented in a separate JavaScript file for modularity and ease of maintenance.

// Save the original title
let originalTitle = document.title;

// Listen for visibility change events
document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
        // Change the title when the tab is inactive
        document.title = "Come back soon! 🛍️";
    } else {
        // Restore the original title when the tab is active again
        document.title = originalTitle;
    }
});

This script is stored in static/js/dynamic_title.js and included site-wide through the base.html template:

{% block extra_js %}
    <script src="{% static 'js/dynamic_title.js' %}"></script>
{% endblock %}

Why This Feature Is Useful

    Improved Retention: Reminds users to return to your site, reducing the chances of them forgetting or abandoning their session.
    Increased Conversions: Helps bring users back to their shopping cart or browsing session, potentially boosting sales.
    Subtle and Non-Intrusive: Does not disrupt the user experience and only displays a message when the user leaves the tab.
    Engaging Messaging: Allows creative and personalized messages, such as "Don’t forget your cart!" or "We miss you already!"

By implementing this feature, your e-commerce site can stay top-of-mind for users and encourage them to re-engage, fostering better retention and conversion rates.

README Update: Adding Confirmation Modals
What We Did

We implemented confirmation modals for deleting products and reviews in the application. These modals are triggered when a user (e.g., a superuser or the review owner) clicks the "Delete" button. Each modal displays a clear message asking the user to confirm their action, with options to either cancel or proceed with the deletion.

    Product Deletion Modal:
        Used in the product details page, specifically for superusers.
        Ensures that deleting a product is intentional.
    Review Deletion Modal:
        Associated with individual reviews in the review section.
        Allows review owners to confirm before deleting their own reviews.

How It Works

    The modals are built using Bootstrap and include:
        A warning message to inform users about the irreversible nature of the action.
        A "Cancel" button to close the modal without taking action.
        A "Delete" button to proceed with the deletion.

    Each modal is dynamically linked to the respective product or review, ensuring the correct item is targeted for deletion.

Why This Improves the Code

    Enhanced User Security:
        Prevents accidental deletions by requiring explicit confirmation from the user.

    Better User Experience:
        Provides clear, non-intrusive feedback to the user before performing critical actions.
        Streamlines the interaction by avoiding unnecessary redirects or reloads for cancellation.

    Dynamic and Scalable:
        The modals are dynamically linked to the respective data (products or reviews), making the solution scalable for multiple items.

    Cleaner UI:
        Maintains a consistent and professional design, aligning with modern web application standards.

This update significantly improves the usability and reliability of deletion functionalities, ensuring that critical actions are always intentional and clear to the user.

Product Review Section Summary

We enhanced the product review section to improve its functionality and user experience. Key updates include:

    Write a Review Button:
        Added a conditional "Write a Review" button visible only to authenticated users who have not yet reviewed the product.
        Users who have already submitted a review see a message indicating so, and unauthenticated users are prompted to log in.

    Review Separation:
        Introduced horizontal lines (<hr>) to visually separate each review, making the layout cleaner and more readable.

    Delete Confirmation Modals:
        Added modals for confirming review deletions, ensuring users cannot accidentally delete reviews without confirmation.

These updates provide a more intuitive and polished interface, aligning with modern e-commerce standards.

Critical Update: SKU Uniqueness Enforcement
Description

In this update, we added a unique constraint to the sku field in the Product model. This ensures that each product has a distinct SKU, a critical identifier used for inventory management, sales tracking, and integration with third-party systems.
Reason for the Change

Previously, the application allowed duplicate SKUs, which led to issues such as:

    Inventory Management Conflicts: Multiple products with the same SKU made it difficult to track stock levels accurately.
    System Integration Errors: Many external systems and APIs (e.g., payment processors, shipping systems) rely on SKU as a unique identifier. Duplicate SKUs caused data mismatches and operational failures.
    User Confusion: Both admin users and customers faced difficulty distinguishing between products with the same SKU.

How the Issue Was Addressed

    Existing Data Cleanup:
        Duplicate SKUs in the database were identified and resolved by appending unique identifiers to affected SKUs.
    Database Schema Update:
        A unique=True constraint was added to the sku field in the Product model to enforce SKU uniqueness at the database level.
    Validation Logic:
        Additional validation was introduced in the model to ensure programmatically created or updated products adhere to the uniqueness rule.

Impact

This change ensures the integrity and reliability of product data, improves system stability during integrations, and enhances the user experience for both admins and customers.

Hero Section

The homepage now features a visually appealing Hero Section designed to engage users immediately upon landing on the site. This section includes:

    Full-Width Hero Image: A dynamic image covering the width of the viewport to create an immersive experience.
    Overlay Design: A semi-transparent overlay ensures the text is legible while maintaining the image's visual impact.
    Structure for Content: The hero section is structured to include a prominent heading, subheading, and a call-to-action button.

Code Highlights:

    HTML:
        Hero section defined with div containers for image and overlay.
        Placeholder for headings and a "Shop Now" button for user engagement.

        Future Enhancements:

    Dynamic Messaging: Add text transitions for marketing messages.
    Interactive Button: Enhance the "Shop Now" button with hover effects or animations.
    Responsive Design: Optimize the hero section for smaller screens and devices.

This feature sets the stage for a visually engaging and user-friendly e-commerce experience.

README Update
About Page Enhancements

The About page was updated with scoped styles to prevent conflicts with global styles from the base CSS. By introducing a unique wrapper class (.about-page), all styles for the About page are isolated and apply exclusively to this page. This approach ensures:

    Modular Design: Scoped styles for better maintainability.
    Conflict Resolution: Avoids overriding global styles like .hero-section.
    Improved Readability: Easier to locate and modify About page styles.

Key updates include:

    Scoped styles for the hero section, profile image, and other page components.
    Adjusted HTML structure by adding a .about-page wrapper for consistent style application.
    Ensured responsive and clean layout across different devices.

This change aligns with modern CSS practices, improving scalability and maintainability of the project.