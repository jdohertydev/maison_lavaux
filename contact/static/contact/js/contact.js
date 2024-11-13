document.addEventListener("DOMContentLoaded", function () {
    const nameField = document.querySelector("#id_name");
    const emailField = document.querySelector("#id_email");

    // Check if the fields are pre-filled (for logged-in users)
    if (nameField && nameField.value.trim() !== "") {
        nameField.setAttribute("readonly", "readonly");
        nameField.style.backgroundColor = "#e9ecef"; // Optional: Grey out for better UX
    }

    if (emailField && emailField.value.trim() !== "") {
        emailField.setAttribute("readonly", "readonly");
        emailField.style.backgroundColor = "#e9ecef"; // Optional: Grey out for better UX
    }
});
