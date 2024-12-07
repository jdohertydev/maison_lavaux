/* jshint esversion: 6 */
/* global $ */

/**
 * Handles styling for the "Country" dropdown in a form.
 *
 * This script ensures that the default styling of the country dropdown 
 * indicates whether a country is selected. If no country is selected, 
 * the text color is set to a placeholder style. When a country is selected, 
 * the text color changes to black.
 */

// Check the initial value of the country dropdown
let countrySelected = $('#id_default_country').val();
if (!countrySelected) {
    // Apply placeholder color for unselected state
    $('#id_default_country').css('color', '#aab7c4');
}

/**
 * Event listener for the "Country" dropdown's change event.
 * Updates the text color based on whether a country is selected.
 */
$('#id_default_country').change(function () {
    countrySelected = $(this).val(); // Get the newly selected value
    if (!countrySelected) {
        // Set placeholder color if no country is selected
        $(this).css('color', '#aab7c4');
    } else {
        // Set normal color for a valid selection
        $(this).css('color', '#000');
    }
});
