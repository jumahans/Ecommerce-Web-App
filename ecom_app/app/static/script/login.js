// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const passwordField = document.querySelector('input[name="password"]');
            const confirmField = document.querySelector('input[name="password_confirm"]');
            
            // If we're on the registration page with password confirmation
            if (passwordField && confirmField) {
                if (passwordField.value !== confirmField.value) {
                    e.preventDefault();
                    
                    // Create error message
                    const errorDiv = document.querySelector('.error');
                    errorDiv.innerHTML = '<p>Passwords do not match!</p>';
                    
                    // Highlight fields
                    passwordField.style.borderColor = 'var(--error-color)';
                    confirmField.style.borderColor = 'var(--error-color)';
                }
            }
        });
        
        // Add input focus effects
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (this.value === '') {
                    this.parentElement.classList.remove('focused');
                }
            });
        });
    }
});