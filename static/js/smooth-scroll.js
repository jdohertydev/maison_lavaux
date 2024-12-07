/* jshint esversion: 6 */
/* jshint browser: true */

/**
 * Initializes a "Back to Top" button functionality.
 * 
 * This script adds an event listener to the document that waits for the DOM content to be fully loaded.
 * Once the content is loaded, it checks for the presence of a "Back to Top" button
 * with the class `.btt-link`. If the button exists, it adds a click event listener
 * that smoothly scrolls the page to the top when the button is clicked.
 */
document.addEventListener('DOMContentLoaded', function () {
    /**
     * Selects the "Back to Top" button using the class `.btt-link`.
     * Ensures that the button exists before attempting to add the event listener.
     */
    const backToTopButton = document.querySelector('.btt-link');
    
    // Check if the button exists on the page
    if (backToTopButton) {
        /**
         * Adds a click event listener to the "Back to Top" button.
         * Prevents the default link behavior and scrolls the page to the top smoothly.
         * 
         * @param {Event} event - The event object representing the click event.
         */
        backToTopButton.addEventListener('click', function (event) {
            event.preventDefault();
            
            // Scrolls the page to the top with a smooth scrolling effect
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});
