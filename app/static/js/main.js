// Hostel Manager - Main JavaScript
// Contains utility functions and event handlers

// Display alert messages
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Format currency
function formatCurrency(value) {
    return '₹' + parseFloat(value).toFixed(2);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN');
}

// Check if email is valid
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Check if phone is valid (10 digits)
function isValidPhone(phone) {
    return /^\d{10}$/.test(phone);
}

// Check if Aadhaar is valid (12 digits)
function isValidAadhaar(aadhaar) {
    return /^\d{12}$/.test(aadhaar);
}

// Confirm action before proceeding
function confirmAction(message) {
    return confirm(message);
}

// Disable button during submission
function disableButton(buttonElement) {
    buttonElement.disabled = true;
    buttonElement.style.opacity = '0.6';
}

// Enable button after submission
function enableButton(buttonElement) {
    buttonElement.disabled = false;
    buttonElement.style.opacity = '1';
}
