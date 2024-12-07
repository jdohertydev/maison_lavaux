/* jshint esversion: 6 */
/* jshint browser: true */

// Store the original page title to restore later
let originalTitle = document.title;

/**
 * Event listener for visibility change.
 * Changes the document title to a custom message when the tab becomes inactive,
 * and restores the original title when the tab becomes active again.
 */
document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
        // Set a custom title when the tab is inactive
        document.title = "Come back soon! 🛍️";
    } else {
        // Restore the original title when the tab becomes active again
        document.title = originalTitle;
    }
});
