/* ==========================================
   1. GESTION VISUELLE (TIROIRS)
   ========================================== */
function toggleInput(label) {
    const inputArea = document.getElementById('input-area-' + label);
    const icon = document.getElementById('icon-' + label);
    const container = document.getElementById('container-' + label);

    if (!inputArea) return;

    if (inputArea.classList.contains('hidden')) {
        inputArea.classList.remove('hidden');
        if(icon) icon.classList.add('rotate-180');
        if(container) {
            container.classList.add('border-indigo-500');
            container.classList.remove('border-gray-200');
        }
        const inputField = inputArea.querySelector('input');
        if (inputField) inputField.focus();
    } else {
        inputArea.classList.add('hidden');
        if(icon) icon.classList.remove('rotate-180');
        if(container) {
            container.classList.remove('border-indigo-500');
            container.classList.add('border-gray-200');
        }
    }
}

/* ==========================================
   2. SÉLECTION D'UNE ADRESSE (VALIDATION)
   ========================================== */
function selectLocation(type, name, lat, lng) {
    const inputVisible = document.getElementById('input-' + type);
    const inputLat = document.getElementById('lat-' + type);
    const inputLng = document.getElementById('lng-' + type);
    const container = document.getElementById('suggestions-' + type);
    const errorMsg = document.getElementById('error-' + type); // Le message d'erreur

    // 1. On remplit les données
    if (inputVisible) inputVisible.value = name;
    if (inputLat) inputLat.value = lat;
    if (inputLng) inputLng.value = lng;

    // 2. On change le style en VERT (Validé)
    if (inputVisible) {
        inputVisible.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        inputVisible.classList.add('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
    }

    // 3. On cache le message d'erreur s'il était là
    if (errorMsg) errorMsg.classList.add('hidden');

    // 4. On vide la liste
    if (container) container.innerHTML = '';
}

/* ==========================================
   3. RECHERCHE (INVALIDATION AUTOMATIQUE)
   ========================================== */
let searchTimeout = null;

async function searchCities(type, query) {
    const container = document.getElementById(`suggestions-${type}`);
    const inputVisible = document.getElementById('input-' + type);
    
    // --- IMPORTANT : DÈS QU'ON TAPE, C'EST INVALIDE ---
    document.getElementById('lat-' + type).value = ""; // On vide la latitude
    document.getElementById('lng-' + type).value = ""; // On vide la longitude
    
    // On enlève le vert (retour au gris normal)
    if (inputVisible) {
        inputVisible.classList.remove('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
        inputVisible.classList.remove('border-red-500'); // On enlève le rouge aussi pour l'instant
    }
    // --------------------------------------------------

    if (!query || query.length < 3) {
        if(container) container.innerHTML = '';
        return;
    }

    if (searchTimeout) clearTimeout(searchTimeout);

    searchTimeout = setTimeout(async () => {
        container.innerHTML = '<div class="p-2 text-xs text-indigo-500 font-bold">Recherche...</div>';
        try {
            // Recherche restreinte à Amiens (80021)
            const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&citycode=80021&limit=5`;
            const response = await fetch(url);
            const data = await response.json();
            
            let htmlContent = '';

            if (data.features && data.features.length > 0) {
                data.features.forEach(feature => {
                    let label = feature.properties.label;
                    const lon = feature.geometry.coordinates[0];
                    const lat = feature.geometry.coordinates[1];
                    const safeName = label.replace(/'/g, "\\'"); 

                    htmlContent += `
                        <button type="button" 
                                onclick="selectLocation('${type}', '${safeName}', ${lat}, ${lon})"
                                class="w-full text-left bg-white hover:bg-indigo-50 text-gray-700 p-3 border-b border-gray-100 text-sm">
                            ${label}
                        </button>`;
                });
            } else {
                htmlContent = '<div class="p-2 text-xs text-gray-400 italic">Adresse inconnue à Amiens</div>';
            }
            container.innerHTML = htmlContent;
        } catch (error) { console.error(error); }
    }, 200);
}

/* ==========================================
   4. VALIDATION AU CLIC SUR "METTRE EN LIGNE"
   ========================================== */
document.querySelector('form').addEventListener('submit', function(event) {
    let isValid = true;

    // Vérification DÉPART
    const latDepart = document.getElementById('lat-depart').value;
    const inputDepart = document.getElementById('input-depart');
    const errorDepart = document.getElementById('error-depart');

    if (!latDepart) {
        // C'est vide ou pas sélectionné -> ERREUR
        event.preventDefault(); // On bloque l'envoi
        isValid = false;
        
        // Style Rouge
        inputDepart.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        // Afficher message
        if (errorDepart) errorDepart.classList.remove('hidden');
        
        // On ouvre le tiroir pour montrer l'erreur
        toggleInput('depart'); 
    }

    // Vérification ARRIVÉE
    const latArrivee = document.getElementById('lat-arrivee').value;
    const inputArrivee = document.getElementById('input-arrivee');
    const errorArrivee = document.getElementById('error-arrivee');

    if (!latArrivee) {
        event.preventDefault();
        isValid = false;
        
        inputArrivee.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        if (errorArrivee) errorArrivee.classList.remove('hidden');
        
        toggleInput('arrivee');
    }

    if (!isValid) {
        // Scroll vers le haut pour voir l'erreur
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});