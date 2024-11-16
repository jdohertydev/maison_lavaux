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
