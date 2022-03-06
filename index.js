window.onload = function() {
    loadButtons();
}

function loadButtons() {
    document.getElementById("loading-submit").addEventListener("click", onSubmit);
}

function onSubmit() {
    var phoneNumberInput = document.getElementById("loading-input").value;
    if (!phoneNumberInput) {
        alert("Please enter a phone number first.");
    } else if (isNaN(phoneNumberInput) || !validateNumber(phoneNumberInput)) {
        document.getElementById("loading-input").value = null;
        alert("This number is invalid.");
    } else {
        window.location.href="home-page.html";
    }
}

function validateNumber(phoneNumberInput) {
    return true;
}