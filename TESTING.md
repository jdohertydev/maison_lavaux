# Validation, Testing and Bugs

- [Validation, Testing and Bugs](#validation-testing-and-bugs)
  - [Validation](#validation)
    - [Manual Testing for PEP8 Compliance](#manual-testing-for-pep8-compliance)
    - [HTML Validation](#html-validation)
    - [CSS Validation](#css-validation)
    - [JS Validation](#js-validation)
    - [Codebase Cleanup](#codebase-cleanup)
  - [Lighthouse Audit Results](#lighthouse-audit-results)
  - [Testing](#testing)
  - [User Stories Testing](#user-stories-testing)
    - [Manual Tests for Acceptance Criteria](#manual-tests-for-acceptance-criteria)
      - [Epic 1: User Experience (UX)](#epic-1-user-experience-ux)
        - [User Story: Minimal Load Times](#user-story-minimal-load-times)
        - [User Story: Seamless Navigation](#user-story-seamless-navigation)
        - [User Story: Clean and Professional Design](#user-story-clean-and-professional-design)
      - [Epic 2: Product Browsing and Reviews](#epic-2-product-browsing-and-reviews)
        - [User Story: Leave a Review](#user-story-leave-a-review)
        - [User Story: Edit or Delete Reviews](#user-story-edit-or-delete-reviews)
        - [User Story: View Detailed Product Information](#user-story-view-detailed-product-information)
        - [User Story: Search for Products](#user-story-search-for-products)
      - [Epic 3: Checkout and Payment](#epic-3-checkout-and-payment)
        - [User Story: Secure Payments via Stripe](#user-story-secure-payments-via-stripe)
        - [User Story: View Order Summary](#user-story-view-order-summary)
      - [Epic 4: Messaging and Communication](#epic-4-messaging-and-communication)
        - [User Story: View All Messages Submitted by Users](#user-story-view-all-messages-submitted-by-users)
        - [User Story: Fill Out a Contact Form](#user-story-fill-out-a-contact-form)
      - [Epic 5: Admin Product Management](#epic-5-admin-product-management)
        - [User Story: Edit Product Details](#user-story-edit-product-details)
        - [User Story: Delete Products](#user-story-delete-products)
        - [User Story: Manage Product Visibility](#user-story-manage-product-visibility)
        - [User Story: Assign Products to Categories](#user-story-assign-products-to-categories)
      - [Epic 6: Sales and Analytics](#epic-6-sales-and-analytics)
        - [User Story: Compare Product Performance](#user-story-compare-product-performance)
        - [User Story: Sort Analytics Data](#user-story-sort-analytics-data)
  - [Manual Testing](#manual-testing)
    - [1. Create Operations](#1-create-operations)
    - [2. Read Operations](#2-read-operations)
    - [3. Update Operations](#3-update-operations)
    - [4. Delete Operations](#4-delete-operations)
    - [5. Edge Cases for Stock Validation](#5-edge-cases-for-stock-validation)
    - [6. Contact Us](#6-contact-us)
    - [7. Review (Edit/Delete)](#7-review-editdelete)
    - [8. Analytics](#8-analytics)
  - [Automated Testing](#automated-testing)
  - [Viewport Testing](#viewport-testing)
    - [Screenshot - Desktop](#screenshot---desktop)
    - [Screenshot - Tablet](#screenshot---tablet)
    - [Screenshot - Mobile](#screenshot---mobile)
  - [Compatibility Testing](#compatibility-testing)
    - [Comparing Chrome and Edge](#comparing-chrome-and-edge)
  - [Bugs](#bugs)
    - [Bug 1: Quantity Controls - Duplicate IDs](#bug-1-quantity-controls---duplicate-ids)
    - [Bug 2: HTML Validation Error - `for` Attribute in Form Label](#bug-2-html-validation-error---for-attribute-in-form-label)
    - [Bug 3: Incorrect Price Display in Order Details](#bug-3-incorrect-price-display-in-order-details)
    - [Bug 4: Pagination Sorting Issue](#bug-4-pagination-sorting-issue)

## Validation

To ensure Python files (.py extensions) are PEP8 valid, the following protocol was followed:

1. **Installing Black**:  
   Black was chosen as a code formatter because it enforces a consistent coding style, improves code readability, and minimizes debates over formatting. It is widely used and trusted within the Python community for its simplicity and efficiency.

   - Command: `$ pip install black`

2. **Updating Requirements**:  
   Updated the `requirements.txt` file to document the inclusion of Black as a development dependency for transparency and future maintainability.

   - Command: `$ pip freeze >> requirements.txt`

3. **Running Black**:  
   Applied Black to the entire project to automatically reformat all `.py` files according to PEP8 standards.

   - Command: `$ black .`

4. **Formatting with Specific Line Length**:  
   Used Black's `--line-length` flag to set the maximum line length to 79 characters, adhering to PEP8 recommendations for readability.

   - Command: `$ black --line-length 79 .`

5. **Manual Validation with CI Python Linter**:  
   After running Black, all `.py` files were manually validated using the CI Python Linter tool. This double-check ensures that the files comply with all PEP8 rules and that no errors were overlooked during formatting.  

   Additionally, I created a script, `list_py_files.py`, to extract and validate the file names of all `.py` files in the project.

   **Why Use CI Python Linter?**  
   The CI Python Linter provides a quick, efficient way to validate PEP8 compliance and highlights issues not automatically resolved by Black, ensuring a higher standard of code quality.

![CI Python Linter Screenshot](readme-images/python-linter-screenshot.png)

### Manual Testing for PEP8 Compliance

These files have been manually tested using CI Python Linter ([https://pep8ci.herokuapp.com/](https://pep8ci.herokuapp.com/)) to ensure compliance with PEP8 standards:

<table>
  <thead>
    <tr>
      <th>Directory</th>
      <th>File</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>/workspace/maison_lavaux/analytics</td>
      <td>admin.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/analytics</td>
      <td>models.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/bag</td>
      <td>contexts.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/bag</td>
      <td>urls.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/bag</td>
      <td>views.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>admin.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>forms.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>models.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>signals.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>urls.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>views.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>webhook_handler.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/checkout</td>
      <td>webhooks.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/contact</td>
      <td>admin.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/contact</td>
      <td>forms.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/contact</td>
      <td>models.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/contact</td>
      <td>urls.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/maison_lavaux</td>
      <td>settings.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/maison_lavaux</td>
      <td>urls.py</td>
      <td>PASS</td>
    </tr>
    <tr>
      <td>/workspace/maison_lavaux/maison_lavaux</td>
      <td>views.py</td>
      <td>PASS</td>
    </tr>
  </tbody>
</table>

### HTML Validation

To validate the HTML code, all static files had to be deployed and checked manually (logged out and logged in where appropriate) using the [Markup Validation Service](https://validator.w3.org/). I created list_html_files.py to extract the file names of all .html files in the project and tested it only on the files I worked on.

<table>
  <thead>
    <tr>
      <th>Directory</th>
      <th>File</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>/bag/templates/bag</td>
      <td>bag.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/bag" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/checkout/templates/checkout</td>
      <td>checkout.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/checkout" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/checkout/templates/checkout</td>
      <td>checkout_success.html</td>
      <td>PASS (Requires dynamic display)</td>
    </tr>
    <tr>
      <td>/contact/templates/contact</td>
      <td>contact.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/contact" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/home/templates/home</td>
      <td>index.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/pages/templates/pages</td>
      <td>about.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/about" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/pages/templates/pages</td>
      <td>privacy_policy.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/privacy-policy" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>add_product.html</td>
      <td>PASS (Requires user login)</td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>add_review.html</td>
      <td>PASS (Requires user login)</td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>confirm_delete_review.html</td>
      <td>PASS (Requires user login)</td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>edit_product.html</td>
      <td>PASS (Requires user login)</td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>edit_review.html</td>
      <td>PASS (Requires user login)</td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>product_detail.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/products/1/" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/products/templates/products</td>
      <td>products.html</td>
      <td><a href="https://validator.w3.org/nu/?doc=https://maison-lavaux-ebcf574677ab.herokuapp.com/products" target="_blank" rel="noopener noreferrer">PASS</a></td>
    </tr>
    <tr>
      <td>/profiles/templates/profiles</td>
      <td>profile.html</td>
      <td>PASS (Requires user login)</td>
    </tr>
    <tr>
      <td>/templates</td>
      <td>400.html</td>
      <td>PASS (Error page)</td>
    </tr>
    <tr>
      <td>/templates</td>
      <td>403.html</td>
      <td>PASS (Error page)</td>
    </tr>
    <tr>
      <td>/templates</td>
      <td>404.html</td>
      <td>PASS (Error page)</td>
    </tr>
    <tr>
      <td>/templates</td>
      <td>500.html</td>
      <td>PASS (Error page)</td>
    </tr>
    <tr>
      <td>/templates/includes/toasts</td>
      <td>toast_error.html</td>
      <td>PASS (Requires dynamic display)</td>
    </tr>
    <tr>
      <td>/templates/includes/toasts</td>
      <td>toast_info.html</td>
      <td>PASS (Requires dynamic display)</td>
    </tr>
    <tr>
      <td>/templates/includes/toasts</td>
      <td>toast_success.html</td>
      <td>PASS (Requires dynamic display)</td>
    </tr>
    <tr>
      <td>/templates/includes/toasts</td>
      <td>toast_warning.html</td>
      <td>PASS (Requires dynamic display)</td>
    </tr>
  </tbody>
</table>

### CSS Validation

To validate the CSS used in the project, I deployed the project on Heroku. Then, I selected the 'View Source' option by right-clicking on the webpage, located 'style.css', and opened it in a separate window. Finally, I ran this code through [The W3C CSS Validation Service - Jigsaw](https://jigsaw.w3.org/css-validator/) for validation. 

The results were as follows:

<table>
  <thead>
    <tr>
      <th>Directory</th>
      <th>File</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>/checkout/static/checkout/css</td>
      <td>checkout.css</td>
      <td><a href="https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fmaison-lavaux.s3.amazonaws.com%2Fstatic%2Fcheckout%2Fcss%2Fcheckout.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en" target="_blank">PASS</a></td>
    </tr>
    <tr>
      <td>/profiles/static/profiles/css</td>
      <td>profile.css</td>
      <td><a href="https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fmaison-lavaux.s3.amazonaws.com%2Fstatic%2Fprofiles%2Fcss%2Fprofile.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en" target="_blank">PASS</a></td>
    </tr>
    <tr>
      <td>/static/css</td>
      <td>about.css</td>
      <td><a href="https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fmaison-lavaux.s3.amazonaws.com%2Fstatic%2Fcss%2Fabout.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en" target="_blank">PASS</a></td>
    </tr>
    <tr>
      <td>/static/css</td>
      <td>base.css</td>
      <td><a href="https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fmaison-lavaux.s3.amazonaws.com%2Fstatic%2Fcss%2Fbase.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en" target="_blank">PASS</a></td>
    </tr>
  </tbody>
</table>

### JS Validation

These files have been manually validated using [JS Hint](https://jshint.com/):

<table>
  <thead>
    <tr>
      <th>Directory</th>
      <th>File</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>/checkout/static/checkout/js</td><td>stripe_elements.js</td><td>PASS</td></tr>
    <tr><td>/contact/static/contact/js</td><td>contact.js</td><td>PASS</td></tr>
    <tr><td>/profiles/static/profiles/js</td><td>countryfield.js</td><td>PASS</td></tr>
    <tr><td>/static/js</td><td>dynamic-messages.js</td><td>PASS</td></tr>
    <tr><td>/static/js</td><td>dynamic_title.js</td><td>PASS</td></tr>
    <tr><td>/static/js</td><td>smooth-scroll.js</td><td>PASS</td></tr>
  </tbody>
</table>

**Screenshot of JSHint Validator for dynamic_title.js**

![Screenshot of JSHint Validator for dynamic_title.js](readme-images/jshint-validator.png)

### Codebase Cleanup

As part of maintaining a clean and organized codebase, the following files were removed:

- `analytics/tests.py`
- `analytics/views.py`
- `bag/admin.py`
- `bag/models.py`
- `bag/tests.py`
- `checkout/tests.py`
- `contact/tests.py`
- `home/admin.py`
- `home/models.py`
- `home/tests.py`
- `pages/admin.py`
- `pages/models.py`
- `pages/tests.py`
- `products/tests.py`
- `profiles/admin.py`
- `profiles/tests.py`

**Reason for Deletion**

It is a good practice to regularly review the project's codebase and remove files that are not contributing to its current functionality. This not only maintains code quality but also ensures that future developers can easily understand and contribute without confusion. Keeping the project clean is key to scalability and maintainability. The rationale behind the removal includes:

1. **Unused Files**: The deleted files were either not used in the project or became redundant as functionality changed during development. Keeping unused files adds unnecessary clutter and makes the codebase harder to maintain and navigate.

2. **Improved Readability**: Removing redundant files significantly improves the readability of the project structure, allowing developers to quickly identify essential components without encountering irrelevant or confusing files.

3. **Reduced Technical Debt**: Actively managing and cleaning the codebase helps reduce technical debt, which ultimately contributes to better project health, maintainability, and long-term sustainability.

4. **Enhanced Collaboration**: A clean project with no unused or redundant files makes it easier for other developers to understand the purpose of each file. This is particularly beneficial when multiple developers are working on the project, as it ensures a shared understanding and reduces the likelihood of duplicated efforts or confusion.

## Lighthouse Audit Results

The site performed well in a Lighthouse, achieving:

- **Performance Score**: 73
- **Accessibility Score**: 87

For comparison, Amazon.co.uk scored:

- **Performance Score**: 83
- **Accessibility Score**: 93

While the results are commendable, these benchmarks indicate room for improvement. Enhancing these metrics could be considered as part of a future feature update to further optimize the user experience.

## Testing

## User Stories Testing

| Epic | User Story | Acceptance Criteria | Result |
|------|------------|---------------------|--------|
| Epic 1: User Experience (UX) | As a user, I can experience minimal load times on every page so that I don't lose interest or abandon the site. | - The website has a clean, consistent, and professional design across all pages.<br>- Responsive design ensures the site is fully functional and visually appealing on desktop, tablet, and mobile devices.<br>- Main navigation and footer are intuitive and accessible on all pages.<br>- Interactive elements (buttons, links, forms) provide clear feedback and are easy to use.<br>- Toast notifications display relevant messages for user actions, such as success, errors, or warnings.<br>- Pages load quickly, with minimal delay even for image-heavy content. | PASS |
| Epic 1: User Experience (UX) | As a user, I can navigate seamlessly across pages so that I can easily find the information or products I need. | - Main navigation menu is visible on all pages and includes links to *Home*, *Shop*, *About Us*, and *Contact Us*.<br>- Navigation menu collapses into a *hamburger menu* on smaller devices and expands correctly when clicked.<br>- Dropdown menus for product categories function smoothly without delays or misalignment.<br>- Footer includes links to *Privacy Policy*, *Terms and Conditions*, and *Customer Support*. | PASS |
| Epic 1: User Experience (UX) | As a user, I can experience a clean and professional design so that I feel confident shopping on a high-quality website. | - Product catalogue displays a grid or list of available items, with each item showing an image, title, price, and rating (if applicable).<br>- Users can filter products by categories, price range, or other attributes.<br>- Users can sort products by relevance, price, or rating.<br>- Pagination or infinite scroll is implemented for seamless browsing of large catalogues.<br>- All product images load without errors, and placeholders are shown for missing images. | PASS |
| Epic 2: Product Browsing and Reviews | As a user, I can leave a review for products I’ve purchased so that I can share my experience with others. | - The website has a clean, consistent, and professional design across all pages.<br>- Responsive design ensures the site is fully functional and visually appealing on desktop, tablet, and mobile devices.<br>- Main navigation and footer are intuitive and accessible on all pages.<br>- Interactive elements (buttons, links, forms) provide clear feedback and are easy to use.<br>- Toast notifications display relevant messages for user actions, such as success, errors, or warnings.<br>- Pages load quickly, with minimal delay even for image-heavy content. | PASS |
| Epic 2: Product Browsing and Reviews | As a user, I can edit or delete my previous reviews so that I can update or remove feedback if necessary. | - Users can edit their reviews directly from the product detail page.<br>- Users can delete their reviews directly from the product detail page.<br>- Editing a review allows users to update the star rating, review title, and comments.<br>- Deleted reviews are removed entirely and no longer visible to other users.<br>- A confirmation prompt appears before a review is deleted.<br>- Editing or deleting a review is restricted to the user who submitted it. | PASS |
| Epic 2: Product Browsing and Reviews | As a user, I can view detailed information (e.g., name, price, description, rating, images) on a product page so that I can make informed purchasing decisions. | - A product page displays the name, price, description, images, and average rating.<br>- Users can scroll through multiple images in a gallery view.<br>- All displayed information is retrieved dynamically from the product database.<br>- An error message appears if a product cannot be loaded. | PASS |
| Epic 2: Product Browsing and Reviews | As a user, I can search for products using keywords so that I can find items quickly. | - A search bar is prominently displayed on the product catalogue page.<br>- Users can input keywords to search for products by name, description, or category.<br>- Search results display relevant products based on the entered keywords.<br>- If no products match the search, a message informs the user that no results were found.<br>- Search functionality works seamlessly across all devices and browsers. | PASS |
| Epic 3: Checkout and Payment | As a user, I can securely pay for my order using Stripe so that I can complete my purchase. | - Users can securely enter payment details on the checkout page.<br>- Payments are processed via Stripe.<br>- Users receive a confirmation message after successful payment. | PASS |
| Epic 3: Checkout and Payment | As a user, I can view a summary of my order total so that I understand the final price I am paying. | - The checkout page displays a breakdown of order total.<br>- Taxes and discounts are clearly shown.<br>- The breakdown updates dynamically with cart changes. | PASS |
| Epic 4: Admin Product Management | As an admin, I can manage product visibility so that items can be hidden when necessary. | - Admins can toggle product visibility in the admin panel.<br>- Hidden products do not appear in the storefront.<br>- Visibility changes are confirmed with a success message. | PASS |
| Epic 4: Admin Product Management | As an admin, I can assign products to categories so that users can find them easily. | - Admins can assign one or more categories to products.<br>- Assigned products appear in the correct category on the storefront.<br>- A confirmation message is displayed after changes. | PASS |
| Epic 5: Admin Product Management | As an admin, I can edit existing product details (e.g., name, price, description, stock) so that the catalogue stays accurate and up-to-date. | - Admins can update product information from the admin panel.<br>- All changes are reflected on the storefront in real-time.<br>- Admins receive a success message after saving changes.<br>- Validation prevents invalid inputs (e.g., negative prices or stock values). | PASS |
| Epic 5: Admin Product Management | As an admin, I can delete products from the catalogue so that discontinued items are no longer displayed. | - Admins can delete products directly from the admin panel.<br>- Deleted products are immediately removed from the storefront and search results.<br>- A confirmation prompt is displayed before deleting a product to prevent accidental removal.<br>- Deleted products are archived in the database for record-keeping. | PASS |
| Epic 6: Sales and Analytics | As an admin, I can compare the performance of multiple products side by side so that I can make informed inventory or marketing decisions. | - Admins can view a dashboard comparing product performance metrics such as sales volume, revenue generated, and customer ratings.<br>- The comparison includes key metrics like total units sold, total revenue, average customer rating, and total page views.<br>- The dashboard allows filtering by product categories and specific date ranges.<br>- Data is displayed in a table format with optional graphical visualisations (e.g., bar charts, line graphs).<br>- Admins can export the comparison data as a CSV file for further analysis. | PASS |
| Epic 6: Sales and Analytics | As an admin, I can sort analytics data (e.g., revenue, views, purchases) so that I can prioritise metrics most relevant to my goals. | - Admins can sort analytics data by metrics such as revenue, page views, and purchases.<br>- Sorting is available in ascending and descending order.<br>- Sortable metrics include total revenue, total views, and purchase counts.<br>- The sorting functionality updates the displayed data immediately.<br>- The sorted view persists until reset or changed by the user. | PASS |

### Manual Tests for Acceptance Criteria

#### Epic 1: User Experience (UX)

##### User Story: Minimal Load Times
**Manual Tests:**
- Tested page load times using **Google Chrome DevTools** and **Lighthouse**.
  - Verified all pages load within 2-3 seconds on desktop and mobile.
  - Ensured image-heavy content loads without blocking user interaction.
- Checked responsive design on multiple devices (desktop, tablet, mobile).
- Verified interactive elements like buttons and links provided visual feedback.
- Triggered actions to test toast notifications for success or error messages.

**Result:** PASS

##### User Story: Seamless Navigation
**Manual Tests:**
- Checked navigation menu links (Home, Shop, About Us, Contact Us) across pages.
- Verified dropdown menus for product categories load and function correctly.
- Tested hamburger menu expansion on smaller devices.
- Verified footer links (Privacy Policy, Terms and Conditions, Customer Support) navigate properly.

**Result:** PASS

##### User Story: Clean and Professional Design
**Manual Tests:**
- Verified product catalogue layout, displaying images, titles, prices, and ratings.
- Tested filtering by categories and price ranges.
- Verified sorting by relevance, price, and rating.
- Checked pagination or infinite scroll functionality for product browsing.
- Ensured all product images load without errors or show placeholders if missing.

**Result:** PASS

#### Epic 2: Product Browsing and Reviews

##### User Story: Leave a Review
**Manual Tests:**
- Submitted reviews for purchased products.
  - Verified reviews appear with correct content and star ratings.
- Tested error handling when submitting incomplete or invalid reviews.

**Result:** PASS

##### User Story: Edit or Delete Reviews
**Manual Tests:**
- Edited reviews from the product detail page.
  - Verified updates reflect immediately on the product page.
- Deleted reviews and confirmed they no longer display.
- Verified a confirmation prompt appears before deletion.
- Tested access control by attempting to edit/delete reviews of other users.

**Result:** PASS

##### User Story: View Detailed Product Information
**Manual Tests:**
- Opened product pages to confirm correct display of name, price, description, images, and ratings.
- Tested scrolling through multiple images in gallery view.
- Triggered error handling for unavailable products.
  
**Result:** PASS

##### User Story: Search for Products
**Manual Tests:**
- Used keywords to search for products by name, description, and category.
- Verified relevant search results are displayed correctly.
- Tested empty search results show a user-friendly message.

**Result:** PASS

#### Epic 3: Checkout and Payment

##### User Story: Secure Payments via Stripe
**Manual Tests:**
- Entered payment details on the checkout page and submitted orders.
- Verified payments are processed via Stripe.
- Checked confirmation message and email receipt after successful payment.

**Result:** PASS

##### User Story: View Order Summary
**Manual Tests:**
- Checked order summary on the checkout page, including taxes and discounts.
- Verified summary updates dynamically with cart changes.

**Result:** PASS

#### Epic 4: Messaging and Communication

##### User Story: View All Messages Submitted by Users

**Manual Tests:**

1. **Submitting a Message:**
   - Filled out the contact form on the website with valid details (name, email, and message).
     - **Example:** Submitted the message: "I have a question about product availability."
     - **Expected Result:** The message was saved to the database and displayed in the admin panel in a structured format.
     - **Actual Result:** The message was correctly saved and appeared under the "Messages" section in the admin panel.

2. **Validating Input Fields:**
   - Tested the contact form with various inputs:
     - **Valid Inputs:** Entered a proper name, valid email address, and a message.
       - **Result:** Form submitted successfully, and a success message was displayed to the user.
     - **Invalid Inputs:** Left the email field blank or entered an incorrectly formatted email.
       - **Expected Result:** Validation error message displayed: "Please enter a valid email address."
       - **Actual Result:** Validation error was shown, and the message was not submitted.

3. **Viewing Messages in Admin Panel:**
   - Navigated to the admin panel and accessed the "Messages" section.
     - **Result:** All submitted messages were displayed with fields for name, email, message content, and submission timestamp.
     - Verified that messages were sorted by the date of submission for easy review.

**Result:** **PASS**

##### User Story: Fill Out a Contact Form

**Manual Tests:**

1. **Filling Out the Form:**
   - Submitted the contact form with valid details (name, email, and message).
     - **Example:** "John Doe, john.doe@example.com, 'What are your shipping times?'"
     - **Expected Result:** A success message was displayed: "Your message has been sent successfully."
     - **Actual Result:** The success message appeared, and the form reset for new input.

2. **Error Handling:**
   - Tested form submission with invalid or missing inputs:
     - Left the message field blank.
       - **Expected Result:** Validation error message displayed: "This field is required."
       - **Actual Result:** Error message appeared, and the form was not submitted.
     - Entered an email in an invalid format (e.g., `not_an_email`).
       - **Expected Result:** Validation error displayed: "Please enter a valid email address."
       - **Actual Result:** Validation error shown, and the message was not submitted.

3. **Database Validation:**
   - Verified that all valid submissions were stored in the database with correct timestamps and linked to the user's account (if logged in).
     - **Result:** Messages appeared in the database table with all fields populated accurately.

**Result:** **PASS**

#### Epic 5: Admin Product Management

##### User Story: Edit Product Details
**Manual Tests:**
- Updated product information (name, price, description, stock) in the admin panel.
- Verified changes reflect on the storefront in real-time.
- Tested validation errors for invalid inputs (e.g., negative prices).

**Result:** PASS

##### User Story: Delete Products
**Manual Tests:**
- Deleted products via the admin panel.
- Confirmed deleted products are removed from the storefront and search results.
- Verified a confirmation prompt prevents accidental deletion.

**Result:** PASS

##### User Story: Manage Product Visibility
**Manual Tests:**
- Toggled product visibility in the admin panel.
- Verified hidden products do not appear on the storefront.
- Checked success messages after visibility updates.

**Result:** PASS

##### User Story: Assign Products to Categories
**Manual Tests:**
- Assigned categories to products in the admin panel.
- Confirmed products display under the correct categories on the storefront.

**Result:** PASS

#### Epic 6: Sales and Analytics

##### User Story: Compare Product Performance
**Manual Tests:**
- Accessed a dashboard displaying metrics like sales, revenue, ratings, and views.
- Tested filters for product categories and date ranges.
- Verified data visualization with bar charts and line graphs.
- Exported comparison data as a CSV file.

**Result:** PASS

##### User Story: Sort Analytics Data
**Manual Tests:**
- Sorted analytics data by revenue, page views, and purchase counts.
- Verified sorting in ascending and descending order updates data immediately.
- Checked persistence of sorted view until reset or changed.

**Result:** PASS

## Manual Testing

Manual testing was conducted to ensure all CRUD (Create, Read, Update, Delete) operations function as expected and handle edge cases gracefully. Below is a detailed summary of the test scenarios performed:

### 1. Create Operations
**Test Scenarios:**
- **Valid Inputs:** Ensured new records (e.g., products, reviews, orders) were successfully created with valid data.
  - **Example:** Adding a new product with all required fields (name, price, category, stock).
  - **Result:** Record created successfully and visible in the frontend.

- **Invalid Inputs:** Tested creation with missing or invalid data.
  - **Example:** Attempted to create a product without a price or category.
  - **Expected Result:** Validation error displayed, record not saved.
  - **Actual Result:** Form prevented submission and displayed an error message: `Price is required.`

### 2. Read Operations
**Test Scenarios:**
- **Valid Data Retrieval:** Verified that all pages correctly display data from the database.
  - **Example:** Viewing the product details page.
  - **Result:** Product information (e.g., name, description, price, stock status) displayed as expected.

- **Edge Cases:**
  - Accessed a non-existent product via direct URL (e.g., `/products/999`).
  - **Expected Result:** Custom 404 error page displayed.
  - **Actual Result:** "Page not found" error page displayed.

### 3. Update Operations
**Test Scenarios:**
- **Valid Update:** Edited existing records using valid inputs.
  - **Example:** Changed a product’s price and stock quantity as an admin.
  - **Result:** Updates reflected immediately in the product list and details page.

- **Invalid Update:** Attempted to update records with invalid inputs.
  - **Example:** Setting a negative price for a product.
  - **Expected Result:** Validation error displayed, update rejected.
  - **Actual Result:** Error message: `Price must be a positive number.`

- **Concurrency Testing:** Tested simultaneous updates by different users.
  - **Example:** Two users updating the same product stock.
  - **Result:** Last update overwrote previous changes, handled without errors.

### 4. Delete Operations
**Test Scenarios:**
- **Valid Deletion:** Successfully deleted records.
  - **Example:** Removed a product from the catalog.
  - **Result:** Product no longer appeared in the frontend or admin panel.

- **Restricted Deletion:** Attempted to delete restricted or related records.
  - **Example:** Tried deleting a product that is part of an active order.
  - **Expected Result:** Error displayed, record not deleted.
  - **Actual Result:** Error: `Cannot delete product linked to existing orders.`

### 5. Edge Cases for Stock Validation
**Test Scenarios:**
- **Zero Stock:**
  - Attempted to add a product with zero stock to the shopping cart.
  - **Expected Result:** Error message displayed: `This product is out of stock.`
  - **Actual Result:** Add-to-cart button disabled, error message displayed.

- **Low Stock:**
  - Added more items to the cart than available in stock.
  - **Expected Result:** Error message: `Only 2 items available.`
  - **Actual Result:** Validation error displayed, cart updated with available quantity.

### 6. Contact Us
**Test Scenarios:**
- **Frontend:**
  - Submitted the form with all valid inputs (name, email, message).
  - **Expected Result:** Success message displayed: `Your message has been sent successfully.`
  - **Actual Result:** Success message displayed and form reset.

- **Backend:**
  - Verified form submissions were stored correctly in the database.
  - **Result:** Contact messages stored with accurate timestamps.

- **Edge Cases:**
  - Submitted form with missing or invalid inputs (e.g., no email).
  - **Expected Result:** Validation error displayed.
  - **Actual Result:** Error: `Please enter a valid email address.`

### 7. Review (Edit/Delete)
**Test Scenarios:**
- **Edit:**
  - Edited an existing review with valid inputs.
  - **Result:** Updated review saved and displayed on the product page.

  - Edited a review with invalid inputs (e.g., blank fields).
  - **Expected Result:** Validation error displayed.
  - **Actual Result:** Error: `Review content cannot be empty.`

- **Delete:**
  - Successfully deleted a review.
  - **Result:** Review removed from both frontend and backend.

  - Attempted to delete another user's review.
  - **Expected Result:** Access denied.
  - **Actual Result:** 403 Forbidden error displayed.

### 8. Analytics
**Test Scenarios:**
- **Valid Data Retrieval:**
  - Viewed product performance metrics (e.g., views, purchases, revenue).
  - **Result:** Data displayed accurately with sortable and filterable columns.

- **Edge Cases:**
  - Filtered data for a time range with no sales or views.
  - **Expected Result:** Empty results displayed with a "No data available" message.
  - **Actual Result:** Correct message displayed.

- **Concurrency:**
  - Tested multiple admins viewing analytics simultaneously.
  - **Result:** No performance issues or data inconsistencies detected.

- **Usability:**
  - Adjusted filters (e.g., date range, top-performing products).
  - **Result:** Filters applied successfully, data updated dynamically.

## Automated Testing

Automated tests were created to ensure the reliability and consistency of the application across various functionalities. These tests primarily focus on the following key areas:

1. **Model Testing**: Verifies the integrity and correctness of the database models, ensuring that fields, methods, and relationships between models behave as expected. For instance:
   - Validation of required fields.
   - Proper functioning of custom model methods (e.g., calculating totals or formatting outputs).

2. **Form Testing**: Ensures that forms validate input data correctly and handle edge cases. This includes:
   - Validating required fields and input constraints (e.g., minimum or maximum length).
   - Testing custom form methods or logic (e.g., pre-filling fields or handling special cases).

3. **View Testing**: Focuses on testing the functionality of views, both class-based and function-based, to confirm:
   - Correct HTTP responses for different scenarios (e.g., GET, POST, invalid requests).
   - Rendering of the expected templates with the correct context data.
   - Proper handling of authentication and authorization for protected views.

4. **URL Testing**: Verifies that all application URLs resolve correctly to the intended views, ensuring seamless navigation and routing.

5. **Admin Panel Testing**: Ensures that customizations in the admin panel, such as list displays, search filters, and actions, function correctly.

6. **Widget Testing**: Tests custom widgets (e.g., dynamic form fields or interactive UI elements) to ensure they work as intended and provide the expected user experience.

7. **Edge Case and Error Testing**: Ensures robust handling of edge cases and unexpected inputs, such as:
   - Submitting invalid data in forms.
   - Accessing restricted pages without proper permissions.

**Purpose of Automated Tests**

Automated tests were implemented to:

- **Enhance Reliability**: By catching bugs and inconsistencies early, the application maintains a high level of quality and stability.
- **Support Refactoring**: Automated tests provide a safety net, ensuring that changes or refactoring do not break existing functionality.
- **Save Time**: Automating repetitive test scenarios reduces manual testing effort and allows for faster iterations during development.
- **Improve Code Coverage**: Comprehensive test coverage ensures that all critical parts of the application are tested, reducing the likelihood of undetected issues in production.

By covering these aspects, the automated tests help maintain a robust and reliable application that can handle diverse user interactions and edge cases effectively.

Below is a summary of the test files and their respective apps, created with assistance from ChatGPT:


| App            | Test File                | Number of Tests | Result |
|----------------|--------------------------|-----------------|--------|
| Analytics      | `test_admin.py`          | 3               | PASS   |
|                | `test_models.py`         | 4               | PASS   |
| Bag            | `test_context.py`        | 3               | PASS   |
|                | `test_views.py`          | 4               | PASS   |
| Products       | `test_forms.py`          | 7               | PASS   |
|                | `test_models.py`         | 8               | PASS   |
|                | `test_urls.py`           | 8               | PASS   |
|                | `test_views.py`          | 4               | PASS   |
|                | `test_widgets.py`        | 2               | PASS   |
| Profiles       | `test_forms.py`          | 6               | PASS   |
|                | `test_models.py`         | 5               | PASS   |
|                | `test_views.py`          | 5               | PASS   |
| Checkout       | `test_admin.py`          | 3               | PASS   |
|                | `test_models.py`         | 4               | PASS   |
|                | `test_signals.py`        | 2               | PASS   |
|                | `test_views.py`          | 8               | PASS   |
| Contact        | `test_admin.py`          | 5               | PASS   |
|                | `test_forms.py`          | 5               | PASS   |
|                | `test_models.py`         | 4               | PASS   |
|                | `test_views.py`          | 8               | PASS   |
| Home           | `test_views.py`          | 8               | PASS   |
| Maison Lavaux  | `test_sitemaps.py`       | 5               | PASS   |

## Viewport Testing

Viewport Testing involved physically testing the project's responsiveness across various devices with different viewports. The test included mobile phones with small and large viewports, as well as tablets. Additionally, testing was conducted on PCs with resolutions of 1366px * 768px (HD) and 1920px * 1080px (Full HD).

### Screenshot - Desktop

![Screenshot - Desktop](readme-images/screenshot-desktop.png)

### Screenshot - Tablet

![Screenshot - Tablet](readme-images/screenshot-tablet.png)

### Screenshot - Mobile

![Screenshot - Mobile](readme-images/screenshot-mobile.png)

After testing, it was confirmed that the content looked great and functioned properly on all tested devices. As a result, the viewport testing was a success, meeting all the expected criteria without any problems.

## Compatibility Testing

The website was tested on all major browsers, including Google Chrome, Mozilla Firefox, Microsoft Edge, Opera, and Safari. The expected outcome was that the project would function correctly in all these browsers.

### Comparing Chrome and Edge

The result showed that there were no functionality issues, all navigation links worked, and the form responded appropriately to empty fields.

![CI Comparing Chrome and Edge](readme-images/chrome-vs-edge.png)

## Bugs

### Bug 1: Quantity Controls - Duplicate IDs

**Priority:** High  
**Severity:** High  

**Description:**  
During the development of the shopping bag functionality, a bug was identified where the quantity increment (+) and decrement (-) buttons did not function properly in the desktop view. This was caused by duplicate IDs assigned to the buttons, with one set for the mobile view and another for the desktop view. Since CSS controlled the visibility of these buttons based on screen size, JavaScript only recognized the first button with the duplicate ID, resulting in functionality issues on other views.

**Steps to Reproduce:**  
1. Add a product to the shopping bag.  
2. Switch between mobile and desktop views.  
3. Attempt to use the quantity increment (+) or decrement (-) buttons in both views.  
4. Observe that only one set of buttons works, depending on the screen size.

**Resolution:**  
- Replaced ID-based selectors with `data-item_id` and `data-size` attributes to uniquely identify elements.
- Updated JavaScript to dynamically locate and handle elements using `data-item_id` and `data-size`.  
- Enhanced logic to:
  - Prevent duplicate handling of increment/decrement buttons.
  - Enable/disable buttons based on the quantity range (1–99).

**Related Code Snippets:**  
```javascript
// Updated JavaScript for handling quantity changes
document.querySelectorAll('[data-item_id]').forEach(button => {
    button.addEventListener('click', function () {
        const itemId = this.getAttribute('data-item_id');
        const size = this.getAttribute('data-size');
        // Logic to handle increment/decrement
    });
});
```

**Impact:**  
- The functionality now works seamlessly across all screen sizes.
- Prevented potential conflicts or errors caused by duplicate IDs in the HTML.

### Bug 2: HTML Validation Error - `for` Attribute in Form Label

**Priority:** Medium  
**Severity:** Low  

**Description:**  
A validation error occurred in the form used to save delivery information. The `<label>` in the unauthenticated user block referenced a `for` attribute (`for="id-save-info"`) that pointed to a non-existent or hidden input field. This violated HTML validation rules, causing accessibility and standards compliance issues.

**Steps to Reproduce:**  
1. Navigate to the checkout page in an unauthenticated state.  
2. Inspect the HTML structure of the `<label>` element.  
3. Observe that the `for` attribute references `id-save-info`, which does not exist in the DOM.  
4. Use the [W3C Validator](https://validator.w3.org/) to confirm the validation error.

**Resolution:**  
- Removed the `for="id-save-info"` attribute from the `<label>` in the unauthenticated user block.
- Adjusted the `<label>` to act as a container for "Create an account" and "Login" links instead.

**Related Code Snippets:**  
```html
<div class="form-check form-check-inline float-right mr-0">
    {% if user.is_authenticated %}
        <label class="form-check-label" for="id-save-info">Save this delivery information to my profile</label>
        <input class="form-check-input ml-2 mr-0" type="checkbox" id="id-save-info" name="save-info" checked>
    {% else %}
        <label class="form-check-label">
            <a class="text-info" href="{% url 'account_signup' %}">Create an account</a> or 
            <a class="text-info" href="{% url 'account_login' %}">login</a> to save this information
        </label>
    {% endif %}
</div>
```

**Impact:**  
- Improved HTML validation, ensuring better accessibility.
- Maintained a seamless user experience for both authenticated and unauthenticated users.

### Bug 3: Incorrect Price Display in Order Details

**Priority:** High  
**Severity:** High  

**Description:**  
On the **checkout success page**, the order details section incorrectly displayed the original price of products, even when a discounted price was applied during checkout. This caused discrepancies between the information displayed to the user and the actual total calculated.

**Steps to Reproduce:**  
1. Add a product with a discounted price to the shopping bag.  
2. Proceed to checkout and complete the payment process.  
3. Observe the **Order Details** section on the checkout success page, where the original price is displayed instead of the discounted price.

**Resolution:**  
- Updated the `checkout_success.html` template to use the `lineitem_total` from the `OrderLineItem` model for price calculations.
- Refactored the `OrderLineItem` model's `save()` method to ensure that `lineitem_total` reflects the discounted price if applicable.

**Related Code Snippets:**  
```python
# OrderLineItem model save() method
def save(self, *args, **kwargs):
    self.lineitem_total = self.product.price * self.quantity
    if self.product.discounted_price:
        self.lineitem_total = self.product.discounted_price * self.quantity
    super().save(*args, **kwargs)
```

**Impact:**  
- Resolved discrepancies in the displayed and calculated prices.  
- Improved user trust by ensuring accurate price information in the order details.

### Bug 4: Pagination Sorting Issue

**Priority:** Medium  
**Severity:** Medium  

**Description:**  
When navigating through paginated product lists, sorting parameters (e.g., `sort` and `direction`) were not persisting, causing inconsistent sorting behavior across pages. This resulted in users experiencing unexpected order changes when moving between pages.

**Steps to Reproduce:**  
1. Navigate to a product list page with pagination enabled.
2. Apply sorting parameters (e.g., sort by price in ascending order).
3. Move to the next page using the "Next" button.
4. Observe that the sorting order is reset to the default, instead of persisting the chosen sorting parameters.

**Resolution:**  
- Updated the pagination logic in the template to dynamically append `sort` and `direction` query parameters to the "Previous" and "Next" links.
- Ensured that sorting options persist across all paginated pages.

**Related Code Snippets:**  
```html
<!-- Updated pagination links in the template -->
<ul class="pagination">
    <li class="page-item">
        <a class="page-link" href="?page={{ page_obj.previous_page_number }}&sort={{ request.GET.sort }}&direction={{ request.GET.direction }}">Previous</a>
    </li>
    <li class="page-item">
        <a class="page-link" href="?page={{ page_obj.next_page_number }}&sort={{ request.GET.sort }}&direction={{ request.GET.direction }}">Next</a>
    </li>
</ul>
```

**Impact:**  
- Improved user experience by ensuring consistent sorting behavior across paginated pages.
- Reduced user frustration caused by unexpected order changes.