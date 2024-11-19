document.addEventListener('DOMContentLoaded', function () {
    const messages = [
        "Discover Your Signature Scent",
        "Find the Perfect Fragrance for Any Occasion",
        "Unleash Your True Essence"
    ];
    const messageContainer = document.querySelector('.dynamic-message');
    let index = 0;

    function showNextMessage() {
        // Fade out the current message
        messageContainer.classList.remove('active');

        // Update the message after fading out
        setTimeout(() => {
            index = (index + 1) % messages.length; // Loop through messages
            messageContainer.textContent = messages[index];
            messageContainer.classList.add('active');
        }, 1000); // Match the fade-out duration
    }

    // Set the initial message and start the loop
    messageContainer.textContent = messages[index];
    messageContainer.classList.add('active');
    setInterval(showNextMessage, 11000); // 10 seconds message display + 1 second fade
});
