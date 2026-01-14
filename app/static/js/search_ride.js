document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([49.8942, 2.2957], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    let routingControl = null;
    let markers = [];
    let destinationMarker = null;
    let searchTimeout = null;

    const placeholder = document.getElementById('map-placeholder');
    const filterInput = document.getElementById('destination-filter');
    const filterCount = document.getElementById('filter-count');
    const suggestionsContainer = document.getElementById('destination-suggestions');
    const clearButton = document.getElementById('clear-filter');
    const latInput = document.getElementById('destination-lat');
    const lonInput = document.getElementById('destination-lon');
    const rideCards = document.querySelectorAll('.ride-card');

    // Geocoding search with autocomplete
    const searchAddress = async (query) => {
        if (!query || query.length < 3) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.classList.add('hidden');
            return;
        }

        if (searchTimeout) clearTimeout(searchTimeout);

        searchTimeout = setTimeout(async () => {
            suggestionsContainer.innerHTML = '<div class="p-3 text-sm text-indigo-500">Recherche...</div>';
            suggestionsContainer.classList.remove('hidden');

            try {
                const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&citycode=80021&limit=5`;
                const response = await fetch(url);
                const data = await response.json();

                if (data.features?.length > 0) {
                    suggestionsContainer.innerHTML = data.features.map(feature => {
                        const label = feature.properties.label;
                        const [lon, lat] = feature.geometry.coordinates;
                        return `
                            <button type="button" 
                                data-lat="${lat}" data-lon="${lon}" data-label="${label.replace(/"/g, '&quot;')}"
                                class="suggestion-btn w-full text-left hover:bg-indigo-50 text-gray-700 p-3 border-b border-gray-100 text-sm transition-colors">
                                <span class="font-medium">${label}</span>
                            </button>`;
                    }).join('');

                    suggestionsContainer.querySelectorAll('.suggestion-btn').forEach(btn => {
                        btn.addEventListener('click', () => selectDestination(btn));
                    });
                } else {
                    suggestionsContainer.innerHTML = '<div class="p-3 text-sm text-gray-400 italic">Aucune adresse trouvée dans la région</div>';
                }
            } catch (error) {
                console.error('Geocoding error:', error);
                suggestionsContainer.innerHTML = '<div class="p-3 text-sm text-red-500">Erreur de recherche</div>';
            }
        }, 300);
    };

    // Select destination from autocomplete
    const selectDestination = (btn) => {
        const lat = parseFloat(btn.dataset.lat);
        const lon = parseFloat(btn.dataset.lon);
        const label = btn.dataset.label;

        filterInput.value = label;
        latInput.value = lat;
        lonInput.value = lon;
        suggestionsContainer.classList.add('hidden');
        clearButton.classList.remove('hidden');

        filterInput.classList.remove('border-gray-300');
        filterInput.classList.add('border-green-500');

        // Add destination marker on map
        if (destinationMarker) {
            map.removeLayer(destinationMarker);
        }

        destinationMarker = L.marker([lat, lon]).addTo(map);
        destinationMarker.bindPopup('<strong>Destination</strong><br>' + label).openPopup();

        map.setView([lat, lon], 13);
        placeholder.classList.add('hidden');

        // Filter rides by proximity to destination (within ~10km)
        filterRidesByDestination(lat, lon);
    };

    // Calculate distance between two points (Haversine formula)
    const calculateDistance = (lat1, lon1, lat2, lon2) => {
        const R = 6371; // Earth's radius in km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    };

    // Filter rides based on destination proximity
    const filterRidesByDestination = (destLat, destLon) => {
        let visibleCount = 0;
        const maxDistance = 1; // km - covers Amiens and surrounding cities

        rideCards.forEach(card => {
            const endLat = parseFloat(card.dataset.endLat);
            const endLon = parseFloat(card.dataset.endLon);
            const distance = calculateDistance(destLat, destLon, endLat, endLon);

            if (distance <= maxDistance) {
                card.classList.remove('hidden');
                visibleCount++;
            } else {
                card.classList.add('hidden');
            }
        });

        filterCount.textContent = `${visibleCount} trajet(s) vers cette destination`;
        filterCount.classList.remove('hidden');
    };

    // Clear filter
    const clearFilter = () => {
        filterInput.value = '';
        latInput.value = '';
        lonInput.value = '';
        clearButton.classList.add('hidden');
        filterCount.classList.add('hidden');
        suggestionsContainer.classList.add('hidden');

        filterInput.classList.remove('border-green-500');
        filterInput.classList.add('border-gray-300');

        if (destinationMarker) {
            map.removeLayer(destinationMarker);
            destinationMarker = null;
        }

        rideCards.forEach(card => card.classList.remove('hidden'));
    };

    // Event listeners
    filterInput.addEventListener('input', (e) => {
        // Reset validation state when typing
        if (latInput.value) {
            latInput.value = '';
            lonInput.value = '';
            filterInput.classList.remove('border-green-500');
            filterInput.classList.add('border-gray-300');
            if (destinationMarker) {
                map.removeLayer(destinationMarker);
                destinationMarker = null;
            }
            rideCards.forEach(card => card.classList.remove('hidden'));
            filterCount.classList.add('hidden');
        }
        searchAddress(e.target.value);
    });

    clearButton.addEventListener('click', clearFilter);

    // Close suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!filterInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.classList.add('hidden');
        }
    });

    // Ride card click handlers
    rideCards.forEach(card => {
        card.addEventListener('click', () => {
            const lat1 = parseFloat(card.dataset.startLat);
            const lon1 = parseFloat(card.dataset.startLon);
            const lat2 = parseFloat(card.dataset.endLat);
            const lon2 = parseFloat(card.dataset.endLon);

            if (routingControl) {
                map.removeControl(routingControl);
                routingControl = null;
            }
            markers.forEach(m => map.removeLayer(m));
            markers = [];

            placeholder.classList.add('hidden');

            routingControl = L.Routing.control({
                waypoints: [L.latLng(lat1, lon1), L.latLng(lat2, lon2)],
                routeWhileDragging: false,
                lineOptions: { styles: [{ color: '#4f46e5', weight: 6 }] },
                createMarker: () => null
            }).addTo(map);

            const m1 = L.marker([lat1, lon1]).addTo(map).bindPopup("Départ");
            const m2 = L.marker([lat2, lon2]).addTo(map).bindPopup("Arrivée");
            markers.push(m1, m2);

            map.fitBounds([[lat1, lon1], [lat2, lon2]], { padding: [50, 50] });

            rideCards.forEach(c => c.classList.remove('ring-2', 'ring-indigo-500'));
            card.classList.add('ring-2', 'ring-indigo-500');
        });
    });

    setTimeout(() => map.invalidateSize(), 200);
});