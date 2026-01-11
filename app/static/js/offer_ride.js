
   // GESTION VISUELLE 
 
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


   // SÉLECTION D'UNE ADRESSE (VALIDATION)
  
function selectLocation(type, name, lat, lng) {
    const inputVisible = document.getElementById('input-' + type);
    const inputLat = document.getElementById('lat-' + type);
    const inputLng = document.getElementById('lng-' + type);
    const container = document.getElementById('suggestions-' + type);
    const errorMsg = document.getElementById('error-' + type); 

    if (inputVisible) inputVisible.value = name;
    if (inputLat) inputLat.value = lat;
    if (inputLng) inputLng.value = lng;

    if (inputVisible) {
        inputVisible.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        inputVisible.classList.add('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
    }

    if (errorMsg) errorMsg.classList.add('hidden');

    if (container) container.innerHTML = '';
}


   // RECHERCHE (INVALIDATION AUTOMATIQUE)

let searchTimeout = null;

async function searchCities(type, query) {
    const container = document.getElementById(`suggestions-${type}`);
    const inputVisible = document.getElementById('input-' + type);
    
    document.getElementById('lat-' + type).value = ""; 
    document.getElementById('lng-' + type).value = ""; 
    
    if (inputVisible) {
        inputVisible.classList.remove('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
        inputVisible.classList.remove('border-red-500'); 
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


   // VALIDATION ET ENVOI DU FORMULAIRE
 
document.querySelector('form').addEventListener('submit', function(event) {
    let isValid = true;

    // 1. Récupération des valeurs
    const latDepart = document.getElementById('lat-depart').value;
    const lngDepart = document.getElementById('lng-depart').value;
    const inputDepart = document.getElementById('input-depart');
    const errorDepart = document.getElementById('error-depart');

    const latArrivee = document.getElementById('lat-arrivee').value;
    const lngArrivee = document.getElementById('lng-arrivee').value;
    const inputArrivee = document.getElementById('input-arrivee');
    const errorArrivee = document.getElementById('error-arrivee');

    [inputDepart, inputArrivee].forEach(input => input.classList.remove('border-red-500'));
    [errorDepart, errorArrivee].forEach(err => { if(err) err.classList.add('hidden'); });

    // Est-ce que les champs sont remplis ?
    if (!latDepart) {
        event.preventDefault();
        isValid = false;
        showError(inputDepart, errorDepart, " Veuillez sélectionner une adresse valide.");
        toggleInput('depart');
    }

    if (!latArrivee) {
        event.preventDefault();
        isValid = false;
        showError(inputArrivee, errorArrivee, " Veuillez sélectionner une adresse valide.");
        if (isValid) toggleInput('arrivee'); // On ouvre seulement si le départ était bon
    }

    // Si les deux sont remplis, on regarde s'ils sont pareils
    if (latDepart && latArrivee && latDepart === latArrivee && lngDepart === lngArrivee) {
        event.preventDefault();
        isValid = false;
        showError(inputArrivee, errorArrivee, " L'arrivée doit être différente du départ !");
        toggleInput('arrivee');
    }

    if (!isValid) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});


function showError(input, errorMsgElement, text) {
    input.classList.remove('border-green-500', 'focus:ring-green-500'); // On enlève le vert
    input.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500'); // On met le rouge
    
    if (errorMsgElement) {
        errorMsgElement.innerText = text; // On change le texte dynamiquement
        errorMsgElement.classList.remove('hidden');
    }
}

   // VALIDATION DATE & HEURE 
   
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('input-jour');
    const timeInput = document.getElementById('input-heure');
    const errorHeure = document.getElementById('error-heure');

    
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
        
        dateInput.addEventListener('input', function() {
            if (this.value && this.value < today) this.value = today;
            verifierHeure(); 
        });
    }

    
    function verifierHeure() {
        if (!dateInput.value || !timeInput.value) return;

        const now = new Date();
        const selectedDate = new Date(dateInput.value);
        const today = new Date();

        
        today.setHours(0,0,0,0);
        selectedDate.setHours(0,0,0,0);

        // Si la date choisie est AUJOURD'HUI
        if (selectedDate.getTime() === today.getTime()) {
            
            // On récupère l'heure actuelle (ex: "14:30")
            const currentHour = now.getHours();
            const currentMin = now.getMinutes();

            // On récupère l'heure saisie (ex: "09:00")
            const [selectedHour, selectedMin] = timeInput.value.split(':').map(Number);

            // COMPARAISON
            if (selectedHour < currentHour || (selectedHour === currentHour && selectedMin < currentMin)) {
                
                timeInput.value = "";
                timeInput.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
                if (errorHeure) errorHeure.classList.remove('hidden');

            } else {
                timeInput.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
                if (errorHeure) errorHeure.classList.add('hidden');
            }
        } else {
            // Si c'est demain ou plus tard, pas de restriction d'heure
            timeInput.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
            if (errorHeure) errorHeure.classList.add('hidden');
        }
    }

    if (timeInput) {
        timeInput.addEventListener('change', verifierHeure);
        timeInput.addEventListener('input', verifierHeure);
    }
});