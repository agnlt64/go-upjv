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

// Fonction pour chercher les villes dynamiquement
async function searchCities(type, query) {
    // 1. On identifie la zone où mettre les boutons (ex: suggestions-depart)
    const container = document.getElementById(`suggestions-${type}`);
    
    // Si la recherche est vide, on ne fait rien (ou on pourrait remettre les suggestions par défaut)
    if (query.length === 0) return;

    try {
        // 2. On interroge notre serveur Python
        const response = await fetch(`/api/recherche-villes?q=${query}`);
        const villes = await response.json();

        // 3. On vide les anciens boutons
        container.innerHTML = '<span class="text-xs text-gray-400 font-bold w-full mb-1 uppercase tracking-wider">Résultats :</span>';

        // 4. On crée les nouveaux boutons
        if (villes.length > 0) {
            villes.forEach(ville => {
                // Création du bouton en HTML pur
                const btnHTML = `
                    <button type="button" 
                            onclick="selectLocation('${type}', \`${ville.name}\`)"
                            class="bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200 text-sm font-medium px-3 py-1.5 rounded-full transition-colors duration-200">
                        ${ville.name}
                    </button>
                `;
                // On l'ajoute au conteneur
                container.innerHTML += btnHTML;
            });
        } else {
            container.innerHTML += '<span class="text-xs text-gray-300 italic">Aucune ville trouvée</span>';
        }

    } catch (error) {
        console.error("Erreur lors de la recherche :", error);
    }
}