/* eslint-env browser */
/* global Stripe, $ */

/**
 * Core logic/payment flow for Stripe integration.
 *
 * Stripe documentation references:
 * - Payment processing: https://stripe.com/docs/payments/accept-a-payment
 * - CSS and styling: https://stripe.com/docs/stripe-js
 */

// Retrieve the Stripe public key and client secret from the DOM
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// Initialize Stripe and its elements
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

/**
 * Define the styling for the Stripe card element.
 * - `base`: General styles for valid input fields.
 * - `invalid`: Styling for invalid input fields.
 */
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create and mount the Stripe card element to the DOM
var card = elements.create('card', { style: style });
card.mount('#card-element');

/**
 * Handles real-time validation errors on the card element.
 * Displays an error message if the user enters invalid card details.
 */
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Get the payment form element
var form = document.getElementById('payment-form');

/**
 * Handles form submission for payment processing.
 * Disables the form during the submission process and displays a loading overlay.
 * Interacts with Stripe's API to confirm the payment.
 *
 * @param {Event} ev - The event object representing the form submission event.
 */
form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    // Disable card input and submit button
    card.update({ disabled: true });
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Check if the user opted to save their information
    var saveInfo = Boolean($('#id-save-info').prop('checked'));
    
    // Get CSRF token for security
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    // Prepare the data for caching on the server
    var postData = {
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: saveInfo,
    };

    // Server endpoint for caching checkout data
    var url = '/checkout/cache_checkout_data/';

    // Cache the data and proceed with payment
    $.post(url, postData)
        .done(function () {
            // Confirm the payment with Stripe
            stripe
                .confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            name: $.trim(form.full_name.value),
                            phone: $.trim(form.phone_number.value),
                            email: $.trim(form.email.value),
                            address: {
                                line1: $.trim(form.street_address1.value),
                                line2: $.trim(form.street_address2.value),
                                city: $.trim(form.town_or_city.value),
                                country: $.trim(form.country.value),
                                state: $.trim(form.county.value),
                            }
                        }
                    },
                    shipping: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        address: {
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            postal_code: $.trim(form.postcode.value),
                            state: $.trim(form.county.value),
                        }
                    },
                })
                .then(function (result) {
                    if (result.error) {
                        // Display error message on failure
                        var errorDiv = document.getElementById('card-errors');
                        var html = `
                            <span class="icon" role="alert">
                                <i class="fas fa-times"></i>
                            </span>
                            <span>${result.error.message}</span>
                        `;
                        $(errorDiv).html(html);
                        $('#payment-form').fadeToggle(100);
                        $('#loading-overlay').fadeToggle(100);
                        card.update({ disabled: false });
                        $('#submit-button').attr('disabled', false);
                    } else {
                        // Submit the form on success
                        if (result.paymentIntent.status === 'succeeded') {
                            form.submit();
                        }
                    }
                });
        })
        .fail(function () {
            // Reload the page to display errors through Django messages
            location.reload();
        });
});
