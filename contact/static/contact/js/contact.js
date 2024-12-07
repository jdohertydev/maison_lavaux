/* jshint esversion: 6 */
/* jshint browser: true */

/**
 * Sets form fields to read-only if they are pre-filled.
 * 
 * This script waits for the DOM content to load before checking specific input fields
 * (e.g., name and email). If these fields are already filled, it makes them read-only
 * to prevent user edits and styles them for better user experience.
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * List of fields to be checked and updated.
     * Each field is represented by its CSS selector and the desired background style.
     */
    const fields = [
        { selector: "#id_name", style: "#e9ecef" },
        { selector: "#id_email", style: "#e9ecef" }
    ];

    /**
     * Iterates through each field configuration.
     * Checks if the field is pre-filled and applies the read-only attribute
     * and background styling if necessary.
     */
    fields.forEach(({ selector, style }) => {
        const field = document.querySelector(selector);
        if (field && field.value.trim() !== "") {
            field.setAttribute("readonly", "readonly"); // Prevent user edits
            field.style.backgroundColor = style; // Apply a styled background
        }
    });
});
