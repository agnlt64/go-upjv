document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const inputs = form.querySelectorAll('input');

    // Regex patterns (from utils.py)
    const UPJV_ID_REGEX = /^[a-zA-Z][0-9]{8}$/;
    const PASSWORD_REGEX = /^(?=.*[a-zA-Z])(?!.*\s)(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
    const EMAIL_REGEX = /^[a-zA-Z]+\.[a-zA-Z]+@([a-zA-Z0-9-]+\.)?u-picardie\.fr$/;
    const PHONE_REGEX = /^[0-9]{10}$/;

    // Field references (cached for performance)
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');

    const showError = (input, message) => {
        const existingError = input.nextElementSibling;

        if (existingError?.classList.contains('error-msg')) {
            existingError.innerText = message;
        } else {
            const errorDiv = document.createElement('p');
            errorDiv.className = 'error-msg text-red-500 text-xs mt-1 font-medium ml-1';
            errorDiv.innerText = message;
            input.parentNode.insertBefore(errorDiv, input.nextSibling);
        }

        input.classList.add('border-red-500', 'ring-1', 'ring-red-500');
        input.classList.remove('border-gray-300', 'focus:border-blue-500', 'focus:ring-blue-500');
    };

    const clearError = (input) => {
        const existingError = input.nextElementSibling;
        if (existingError?.classList.contains('error-msg')) {
            existingError.remove();
        }
        input.classList.remove('border-red-500', 'ring-1', 'ring-red-500');
        input.classList.add('border-gray-300', 'focus:border-blue-500', 'focus:ring-blue-500');
    };

    const validateInput = (input) => {
        const value = input.value.trim();
        const id = input.id;

        if (input.hasAttribute('required') && value === '') {
            return false;
        }

        let errorMessage = '';

        switch (id) {
            case 'upjv_id':
                if (!UPJV_ID_REGEX.test(value)) {
                    errorMessage = 'Identifiant invalide (1 lettre + 8 chiffres).';
                }
                break;

            case 'email':
                if (!EMAIL_REGEX.test(value)) {
                    errorMessage = 'Email invalide (format: prenom.nom@u-picardie.fr).';
                }
                break;

            case 'phone_number':
                if (!PHONE_REGEX.test(value)) {
                    errorMessage = 'Numéro invalide (10 chiffres).';
                }
                break;
 
            case 'password':
                if (!PASSWORD_REGEX.test(input.value)) {
                    const errors = [];
                    if (input.value.length < 8) errors.push('8 caractères');
                    if (!/[a-zA-Z]/.test(input.value)) errors.push('1 lettre');
                    if (/\s/.test(input.value)) errors.push("pas d'espaces");
                    if (!/\d/.test(input.value)) errors.push('1 chiffre');
                    if (!/[!@#$%^&*(),.?":{}|<>]/.test(input.value)) errors.push('1 caractère spécial');
                    errorMessage = 'Manque : ' + errors.join(', ');
                }
                break;

            case 'confirm_password':
                if (passwordInput && input.value !== passwordInput.value) {
                    errorMessage = 'Les mots de passe ne correspondent pas.';
                }
                break;
        }

        if (errorMessage) {
            showError(input, errorMessage);
            return false;
        }

        clearError(input);
        return true;
    };

    const checkFormValidity = () => {
        let formIsValid = true;

        inputs.forEach(input => {
            if (input.hasAttribute('required') && input.value.trim() === '') formIsValid = false;
            if (input.classList.contains('border-red-500')) formIsValid = false;
        });

        submitBtn.disabled = !formIsValid;
        submitBtn.classList.toggle('opacity-50', !formIsValid);
        submitBtn.classList.toggle('cursor-not-allowed', !formIsValid);
        submitBtn.classList.toggle('hover:translate-x-1', formIsValid);
        submitBtn.classList.toggle('cursor-pointer', formIsValid);
    };

    inputs.forEach(input => {
        input.addEventListener('input', () => {
            validateInput(input);
            if (input.id === 'password' && confirmInput?.value) {
                validateInput(confirmInput);
            }
            checkFormValidity();
        });

        input.addEventListener('blur', () => {
            if (input.hasAttribute('required') && input.value.trim() === '') {
                showError(input, 'Ce champ est requis.');
            } else {
                validateInput(input);
            }
            checkFormValidity();
        });
    });

    checkFormValidity();
});