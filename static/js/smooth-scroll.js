document.addEventListener('DOMContentLoaded', function () {
    const backToTopButton = document.querySelector('.btt-link');
    if (backToTopButton) { // Check if the button exists on the page
        backToTopButton.addEventListener('click', function (event) {
            event.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});