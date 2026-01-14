const $ = (id) => document.getElementById(id);

let searchTimeout = null;

const toggleInput = (label) => {
    const inputArea = $(`input-area-${label}`);
    const icon = $(`icon-${label}`);
    const container = $(`container-${label}`);

    if (!inputArea) return;

    const isHidden = inputArea.classList.contains('hidden');
    inputArea.classList.toggle('hidden', !isHidden);

    if (icon) icon.classList.toggle('rotate-180', isHidden);
    if (container) {
        container.classList.toggle('border-indigo-500', isHidden);
        container.classList.toggle('border-gray-200', !isHidden);
    }

    if (isHidden) {
        const inputField = inputArea.querySelector('input');
        if (inputField) inputField.focus();
    }
};

const selectLocation = (type, name, lat, lng) => {
    const inputVisible = $(`input-${type}`);
    const inputLat = $(`lat-${type}`);
    const inputLng = $(`lng-${type}`);
    const container = $(`suggestions-${type}`);
    const errorMsg = $(`error-${type}`);

    if (inputVisible) inputVisible.value = name;
    if (inputLat) inputLat.value = lat;
    if (inputLng) inputLng.value = lng;

    if (inputVisible) {
        inputVisible.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        inputVisible.classList.add('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
    }

    if (errorMsg) errorMsg.classList.add('hidden');
    if (container) container.innerHTML = '';
};

const searchCities = async (type, query) => {
    const container = $(`suggestions-${type}`);
    const inputVisible = $(`input-${type}`);

    $(`lat-${type}`).value = '';
    $(`lng-${type}`).value = '';

    if (inputVisible) {
        inputVisible.classList.remove('border-green-500', 'focus:border-green-500', 'focus:ring-green-500', 'border-red-500');
    }

    if (!query || query.length < 3) {
        if (container) container.innerHTML = '';
        return;
    }

    if (searchTimeout) clearTimeout(searchTimeout);

    searchTimeout = setTimeout(async () => {
        container.innerHTML = '<div class="p-2 text-xs text-indigo-500 font-bold">Recherche...</div>';

        try {
            const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&citycode=80021&limit=5`;
            const response = await fetch(url);
            const data = await response.json();

            if (data.features?.length > 0) {
                container.innerHTML = data.features.map(feature => {
                    const label = feature.properties.label;
                    const [lon, lat] = feature.geometry.coordinates;
                    const safeName = label.replace(/'/g, "\\'");
                    return `
                        <button type="button" 
                            data-location='{"type":"${type}","name":"${safeName}","lat":${lat},"lon":${lon}}'
                            class="suggestion-btn w-full text-left bg-white hover:bg-indigo-50 text-gray-700 p-3 border-b border-gray-100 text-sm">
                            ${label}
                        </button>`;
                }).join('');

                container.querySelectorAll('.suggestion-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const loc = JSON.parse(btn.dataset.location);
                        selectLocation(loc.type, loc.name, loc.lat, loc.lon);
                    });
                });
            } else {
                container.innerHTML = '<div class="p-2 text-xs text-gray-400 italic">Adresse inconnue à Amiens</div>';
            }
        } catch (error) {
            console.error(error);
        }
    }, 200);
};

const showError = (input, errorMsgElement, text) => {
    input.classList.remove('border-green-500', 'focus:ring-green-500');
    input.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');

    if (errorMsgElement) {
        errorMsgElement.innerText = text;
        errorMsgElement.classList.remove('hidden');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const form = $('offer-ride-form');
    const dateInput = $('input-jour');
    const timeInput = $('input-heure');
    const errorHeure = $('error-heure');
    const inputDepart = $('input-depart');
    const inputArrivee = $('input-arrivee');
    const seatsInput = $('input-seats');

    // Toggle handlers for offer_ride sections
    document.querySelectorAll('.offer-ride-toggle').forEach(toggle => {
        toggle.addEventListener('click', () => {
            toggleInput(toggle.dataset.toggle);
        });
    });

    // City search handlers
    inputDepart?.addEventListener('input', (e) => searchCities('depart', e.target.value));
    inputArrivee?.addEventListener('input', (e) => searchCities('arrivee', e.target.value));

    // Stop propagation for inputs inside collapsible sections
    [timeInput, dateInput, seatsInput].forEach(input => {
        input?.addEventListener('click', (e) => e.stopPropagation());
    });

    // Max seats validation
    if (seatsInput) {
        const maxSeats = parseInt(seatsInput.dataset.max);
        seatsInput.addEventListener('input', () => {
            if (parseInt(seatsInput.value) > maxSeats) {
                seatsInput.value = maxSeats;
            }
        });
    }

    // Date validation
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);

        dateInput.addEventListener('input', function () {
            if (this.value && this.value < today) this.value = today;
            validateTime();
        });
    }

    const validateTime = () => {
        if (!dateInput?.value || !timeInput?.value) return;

        const now = new Date();
        const selectedDate = new Date(dateInput.value);
        const todayDate = new Date();
        todayDate.setHours(0, 0, 0, 0);
        selectedDate.setHours(0, 0, 0, 0);

        const isToday = selectedDate.getTime() === todayDate.getTime();

        if (isToday) {
            const [selectedHour, selectedMin] = timeInput.value.split(':').map(Number);
            const isPast = selectedHour < now.getHours() ||
                (selectedHour === now.getHours() && selectedMin < now.getMinutes());

            if (isPast) {
                timeInput.value = '';
                timeInput.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
                errorHeure?.classList.remove('hidden');
                return;
            }
        }

        timeInput.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        errorHeure?.classList.add('hidden');
    };

    if (timeInput) {
        timeInput.addEventListener('change', validateTime);
        timeInput.addEventListener('input', validateTime);
    }

    // Form validation
    if (form) {
        form.addEventListener('submit', (event) => {
            const latDepart = $('lat-depart')?.value;
            const latArrivee = $('lat-arrivee')?.value;
            const lngDepart = $('lng-depart')?.value;
            const lngArrivee = $('lng-arrivee')?.value;

            const errorDepart = $('error-depart');
            const errorArrivee = $('error-arrivee');

            [inputDepart, inputArrivee].forEach(input => input?.classList.remove('border-red-500'));
            [errorDepart, errorArrivee].forEach(err => err?.classList.add('hidden'));

            let isValid = true;

            if (!latDepart) {
                event.preventDefault();
                isValid = false;
                showError(inputDepart, errorDepart, "Veuillez sélectionner une adresse valide.");
                toggleInput('depart');
            }

            if (!latArrivee) {
                event.preventDefault();
                isValid = false;
                showError(inputArrivee, errorArrivee, "Veuillez sélectionner une adresse valide.");
                if (latDepart) toggleInput('arrivee');
            }

            if (latDepart && latArrivee && latDepart === latArrivee && lngDepart === lngArrivee) {
                event.preventDefault();
                isValid = false;
                showError(inputArrivee, errorArrivee, "L'arrivée doit être différente du départ !");
                toggleInput('arrivee');
            }

            if (!isValid) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    // ===== EDIT RIDE MODAL =====
    const modal = $('edit-ride-modal');
    const editForm = $('edit-ride-form');
    const closeBtn = $('close-edit-modal');
    const cancelBtn = $('cancel-edit-btn');
    const errorMsg = $('edit-error-message');

    if (!modal || !editForm) return; // Skip if modal doesn't exist

    let editSearchTimeout = null;

    // Open modal when clicking on ride card
    document.querySelectorAll('.edit-ride-btn').forEach(card => {
        card.addEventListener('click', () => {
            $('edit-ride-id').value = card.dataset.rideId;
            $('edit-ride-date').value = card.dataset.rideDate;
            $('edit-ride-time').value = card.dataset.rideTime;
            $('edit-ride-seats').value = card.dataset.rideSeats;
            $('edit-start-location').value = card.dataset.startName;
            $('edit-start-lat').value = card.dataset.startLat;
            $('edit-start-lon').value = card.dataset.startLon;
            $('edit-end-location').value = card.dataset.endName;
            $('edit-end-lat').value = card.dataset.endLat;
            $('edit-end-lon').value = card.dataset.endLon;

            // Mark inputs as valid initially
            ['edit-start-location', 'edit-end-location'].forEach(id => {
                $(id).classList.add('border-green-500');
                $(id).classList.remove('border-gray-300');
            });

            errorMsg?.classList.add('hidden');
            modal.classList.remove('hidden');
        });
    });

    // Close modal
    const closeModal = () => {
        modal.classList.add('hidden');
        editForm.reset();
        errorMsg?.classList.add('hidden');
    };

    closeBtn?.addEventListener('click', closeModal);
    cancelBtn?.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Address autocomplete for edit modal
    const searchEditAddress = async (type, query) => {
        const container = $(`edit-suggestions-${type}`);
        const latInput = $(`edit-${type}-lat`);
        const lonInput = $(`edit-${type}-lon`);
        const textInput = $(`edit-${type}-location`);

        // Clear validation when typing
        latInput.value = '';
        lonInput.value = '';
        textInput.classList.remove('border-green-500');
        textInput.classList.add('border-gray-300');

        if (!query || query.length < 3) {
            container.classList.add('hidden');
            return;
        }

        if (editSearchTimeout) clearTimeout(editSearchTimeout);

        editSearchTimeout = setTimeout(async () => {
            try {
                const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&citycode=80021&limit=5`;
                const response = await fetch(url);
                const data = await response.json();

                if (data.features?.length > 0) {
                    container.innerHTML = data.features.map(f => {
                        const [lon, lat] = f.geometry.coordinates;
                        return `<button type="button" class="edit-suggestion w-full text-left p-2 hover:bg-indigo-50 text-sm border-b border-gray-100"
                            data-type="${type}" data-lat="${lat}" data-lon="${lon}" data-name="${f.properties.label.replace(/"/g, '&quot;')}">
                            ${f.properties.label}
                        </button>`;
                    }).join('');

                    container.querySelectorAll('.edit-suggestion').forEach(btn => {
                        btn.addEventListener('click', () => {
                            textInput.value = btn.dataset.name;
                            latInput.value = btn.dataset.lat;
                            lonInput.value = btn.dataset.lon;
                            textInput.classList.add('border-green-500');
                            textInput.classList.remove('border-gray-300');
                            container.classList.add('hidden');
                        });
                    });

                    container.classList.remove('hidden');
                } else {
                    container.innerHTML = '<div class="p-2 text-sm text-gray-400 italic">Aucune adresse trouvée</div>';
                    container.classList.remove('hidden');
                }
            } catch (e) {
                console.error(e);
            }
        }, 200);
    };

    $('edit-start-location')?.addEventListener('input', (e) => searchEditAddress('start', e.target.value));
    $('edit-end-location')?.addEventListener('input', (e) => searchEditAddress('end', e.target.value));

    // Edit form submission
    editForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const startLat = $('edit-start-lat').value;
        const endLat = $('edit-end-lat').value;

        if (!startLat || !endLat) {
            errorMsg.textContent = 'Veuillez sélectionner des adresses valides dans les suggestions.';
            errorMsg.classList.remove('hidden');
            return;
        }

        const rideId = $('edit-ride-id').value;
        const formData = new FormData(editForm);

        try {
            const response = await fetch(`/api/update-ride/${rideId}`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                window.location.reload();
            } else {
                errorMsg.textContent = data.message;
                errorMsg.classList.remove('hidden');
            }
        } catch (err) {
            errorMsg.textContent = 'Une erreur est survenue.';
            errorMsg.classList.remove('hidden');
        }
    });
});