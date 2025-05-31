// static/script.js
function confirmDelete(event) {
    if (!confirm('Are you sure you want to remove this phone number?')) {
        event.preventDefault(); // Stop form submission if user cancels
    }
}

// Add event listeners after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const deleteForms = document.querySelectorAll('form.delete-form'); // Target forms specifically
    deleteForms.forEach(form => {
        form.addEventListener('submit', confirmDelete);
    });
});
