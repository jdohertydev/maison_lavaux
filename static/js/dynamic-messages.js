/* jshint esversion: 6 */
/* jshint browser: true */

/**
 * Handles dynamic rotation of promotional messages on page load.
 * The messages fade out and are replaced by the next one in the sequence.
 */
document.addEventListener('DOMContentLoaded', function () {
    const messages = [
        "Discover Your Signature Scent", // Message 1
        "Find the Perfect Fragrance for Any Occasion", // Message 2
        "Unleash Your True Essence" // Message 3
    ];
    const messageContainer = document.querySelector('.dynamic-message');
    let index = 0;

    /**
     * Displays the next message with a fade-out and fade-in effect.
     * Updates the content and loops through the message array.
     */
    function showNextMessage() {
        // Fade out the current message
        messageContainer.classList.remove('active');

        // Update the message after fading out
        setTimeout(() => {
            index = (index + 1) % messages.length; // Loop through messages
            messageContainer.textContent = messages[index];
            messageContainer.classList.add('active'); // Fade in the new message
        }, 1000); // Match the fade-out duration
    }

    // Set the initial message and start the loop
    messageContainer.textContent = messages[index];
    messageContainer.classList.add('active');
    setInterval(showNextMessage, 11000); // 10 seconds message display + 1 second fade
});
