document.addEventListener('DOMContentLoaded', () => {
    try {
        const form = document.querySelector('form');
        if (!form) return;

        const submitBtn = form.querySelector('button[type="submit"]');
        const inputs = form.querySelectorAll('input');

        // --- FONCTIONS D'AFFICHAGE ---

        const showError = (input, message) => {
            let existingError = input.nextElementSibling;
            
            if (existingError && existingError.classList.contains('error-msg')) {
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
            if (existingError && existingError.classList.contains('error-msg')) {
                existingError.remove();
            }
            input.classList.remove('border-red-500', 'ring-1', 'ring-red-500');
            input.classList.add('border-gray-300', 'focus:border-blue-500', 'focus:ring-blue-500');
        };

        // --- VALIDATION ---

        const validateInput = (input) => {
            const value = input.value;
            const id = input.id;
            let isValid = true;
            let errorMessage = "";

            try {
                if (input.hasAttribute('required') && value.trim() === '') {
                    return false; 
                }

                if (id === 'upjv_id') {
                    if (value.trim().length < 3) {
                        isValid = false;
                        errorMessage = "Identifiant invalide.";
                    }
                }

                if (id === 'email') {
                    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim())) {
                        isValid = false;
                        errorMessage = "Email invalide.";
                    }
                }

                if (id === 'phone_number') {
                    const cleanPhone = value.replace(/\D/g, '');
                    if (cleanPhone.length < 10) {
                        isValid = false;
                        errorMessage = "Numéro invalide (10 chiffres).";
                    } else if (cleanPhone.length > 10) {
                        isValid = false;
                        errorMessage = "Numéro trop long (max 10 chiffres).";
                    }
                }

                if (id === 'password') {
                    const isSignUp = document.getElementById('confirm_password') !== null;

                    if (isSignUp) {
                        let errors = [];
                        
                        if (value.length < 8) errors.push("8 caractères");
                        if (!/[A-Z]/.test(value)) errors.push("1 majuscule");
                        if (!/\d/.test(value)) errors.push("1 chiffre");
                        if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) errors.push("1 caractère spécial");

                        if (errors.length > 0) {
                            isValid = false;
                            errorMessage = "Manque : " + errors.join(", ");
                        }
                    } else {
                         if (value.length < 1) isValid = false;
                    }
                }

                if (id === 'confirm_password') {
                    const passwordInput = document.getElementById('password');
                    if (passwordInput && value !== passwordInput.value) {
                        isValid = false;
                        errorMessage = "Les mots de passe ne correspondent pas.";
                    }
                }

                if (!isValid && errorMessage !== "") {
                    showError(input, errorMessage);
                } else if (isValid) {
                    clearError(input);
                }

                return isValid;

            } catch (err) {
                console.error(err);
                return false;
            }
        };

        // --- ÉTAT DU FORMULAIRE ---

        const checkFormValidity = () => {
            let formIsValid = true;
            inputs.forEach(input => {
                if (input.hasAttribute('required') && input.value.trim() === '') formIsValid = false;
                if (input.classList.contains('border-red-500')) formIsValid = false;
            });

            if (formIsValid) {
                submitBtn.removeAttribute('disabled');
                submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                submitBtn.classList.add('hover:translate-x-1', 'cursor-pointer');
            } else {
                submitBtn.setAttribute('disabled', 'true');
                submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
                submitBtn.classList.remove('hover:translate-x-1', 'cursor-pointer');
            }
        };

        // --- ÉCOUTEURS ---

        inputs.forEach(input => {
            input.addEventListener('input', () => {
                validateInput(input);
                if (input.id === 'password') {
                    const confirmInput = document.getElementById('confirm_password');
                    if (confirmInput && confirmInput.value !== '') validateInput(confirmInput);
                }
                checkFormValidity();
            });

            input.addEventListener('blur', () => {
                if (input.hasAttribute('required') && input.value.trim() === '') {
                    showError(input, "Ce champ est requis.");
                } else {
                    validateInput(input);
                }
                checkFormValidity();
            });
        });

        checkFormValidity();

    } catch (e) {
        console.error("Auth JS Error:", e);
    }
});