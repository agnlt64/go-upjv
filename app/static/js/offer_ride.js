/* ==========================================
   1. GESTION DE L'INTERFACE (OUVERTURE/FERMETURE)
   ========================================== */

function toggleInput(label) {
    const inputArea = document.getElementById('input-area-' + label);
    const icon = document.getElementById('icon-' + label);
    const container = document.getElementById('container-' + label);

    if (!inputArea) return;

    if (inputArea.classList.contains('hidden')) {
        // --- OUVERTURE ---
        inputArea.classList.remove('hidden');
        
        if(icon) icon.classList.add('rotate-180');
        
        if(container) {
            container.classList.add('border-indigo-500');
            container.classList.remove('border-gray-200');
        }

        // Focus automatique sur le champ
        const inputField = inputArea.querySelector('input');
        if (inputField) {
            inputField.focus();
            if (inputField.type === 'date' || inputField.type === 'time') {
                try { inputField.showPicker(); } catch (e) {}
            }
        }

    } else {
        // --- FERMETURE ---
        inputArea.classList.add('hidden');
        
        if(icon) icon.classList.remove('rotate-180');

        if(container) {
            container.classList.remove('border-indigo-500');
            container.classList.add('border-gray-200');
        }
    }
}


/* ==========================================
   2. GESTION DE LA SÉLECTION D'ADRESSE
   ========================================== */

function selectLocation(type, name, lat, lng) {
    // 1. Remplir le champ visible
    const inputVisible = document.getElementById('input-' + type);
    if (inputVisible) {
        inputVisible.value = name;
    }

    // 2. Remplir les champs cachés (Latitude / Longitude)
    const inputLat = document.getElementById('lat-' + type);
    const inputLng = document.getElementById('lng-' + type);
    
    // Note : On s'assure que ce sont des nombres
    if (inputLat) inputLat.value = lat;
    if (inputLng) inputLng.value = lng;

    console.log(`📍 Sélectionné pour ${type}: ${name} (${lat}, ${lng})`);

    // 3. Vider la liste des suggestions
    const container = document.getElementById(`suggestions-${type}`);
    if (container) container.innerHTML = '';
}


/* ==========================================
   3. RECHERCHE API GOUVERNEMENT (BAN)
   ========================================== */

let searchTimeout = null;

async function searchCities(type, query) {
    const container = document.getElementById(`suggestions-${type}`);
    
    // Si moins de 3 lettres, on vide et on arrête
    if (!query || query.length < 3) {
        if(container) container.innerHTML = '';
        return;
    }

    // On annule la recherche précédente si l'utilisateur tape encore
    if (searchTimeout) clearTimeout(searchTimeout);

    // On attend 200ms avant de lancer la requête (debounce)
    searchTimeout = setTimeout(async () => {
        
        container.innerHTML = '<div class="p-2 text-xs text-indigo-500 font-bold animate-pulse">Recherche en cours...</div>';

        try {
            const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&citycode=80021&limit=5`;
            const response = await fetch(url);
            const data = await response.json();
            
            // On prépare le HTML
            let htmlContent = '<div class="w-full px-2 py-1 text-xs text-gray-400 font-bold uppercase tracking-wider">Suggestions :</div>';

            if (data.features && data.features.length > 0) {
                data.features.forEach(feature => {
                    const label = feature.properties.label;     // Ex: "8 Boulevard du Port, Amiens"
                    const lon = feature.geometry.coordinates[0]; // Attention API BAN = [Lon, Lat]
                    const lat = feature.geometry.coordinates[1]; 

                    if (label.endsWith(',')) label = label.slice(0, -1);

                    const safeName = feature.properties.label.replace(/'/g, "\\'");

                    htmlContent += `
                        <button type="button" 
                                onclick="selectLocation('${type}', '${safeName}', ${lat}, ${lon})"
                                class="w-full text-left bg-white hover:bg-indigo-50 text-gray-700 hover:text-indigo-700 border-b last:border-0 border-gray-100 px-4 py-3 transition-colors duration-150 flex items-center group">
                            <svg class="w-4 h-4 mr-3 text-gray-400 group-hover:text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                            <span class="truncate font-medium text-sm">${label}</span>
                        </button>
                    `;
                });
            } else {
                htmlContent = '<div class="p-2 text-xs text-gray-400 italic">Aucune adresse trouvée</div>';
            }
            
            container.innerHTML = htmlContent;

        } catch (error) {
            console.error("Erreur API :", error);
            container.innerHTML = '<div class="p-2 text-xs text-red-400">Erreur de connexion</div>';
        }

    }, 200);
}


/* ==========================================
   4. INITIALISATION (DATE DU JOUR)
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('input-jour');

    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
        
        dateInput.addEventListener('input', function() {
            if (this.value && this.value < today) {
                this.value = today; 
            }
        });
    }
});