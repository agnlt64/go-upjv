function toggleInput(label) {
    const inputArea = document.getElementById('input-area-' + label);
    const icon = document.getElementById('icon-' + label);
    const container = document.getElementById('container-' + label);

    if (!inputArea) return;

    if (inputArea.classList.contains('hidden')) {
        // --- OUVERTURE ---
        inputArea.classList.remove('hidden');
        
        if(icon) icon.classList.add('rotate-180');
        
        container.classList.add('border-indigo-500');
        container.classList.remove('border-gray-200');

        // FOCUS AMÉLIORÉ
        const inputField = inputArea.querySelector('input');
        if (inputField) {
            inputField.focus();
            // Si c'est une date ou une heure, on essaie d'ouvrir le sélecteur natif
            if (inputField.type === 'date' || inputField.type === 'time') {
                try {
                    inputField.showPicker(); 
                } catch (e) {
                    // Si le navigateur est trop vieux, il ne fera rien (pas grave)
                }
            }
        }

    } else {
        // --- FERMETURE ---
        inputArea.classList.add('hidden');
        
        if(icon) icon.classList.remove('rotate-180');

        container.classList.remove('border-indigo-500');
        container.classList.add('border-gray-200');
    }
}

function selectLocation(fieldId, value) {
    const input = document.getElementById('input-' + fieldId);
    
    if (input) {
        input.value = value;
    }
}

    document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('input-jour');

    if (dateInput) {
        // 1. Date du jour
        const today = new Date().toISOString().split('T')[0];

        // 2. On bloque visuellement le calendrier (attribut min)
        dateInput.setAttribute('min', today);

        // 3. Surveillance de la saisie
        dateInput.addEventListener('input', function() {
            // Si la date est remplie ET qu'elle est dans le passé
            if (this.value && this.value < today) {
                
                // On force la date d'aujourd'hui
                this.value = today; 

            }
        });
    }
});