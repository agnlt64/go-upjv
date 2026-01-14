document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([49.8942, 2.2957], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    let routingControl = null;
    let markers = [];
    let destinationMarker = null;
    const placeholder = document.getElementById('map-placeholder');
    const filterInput = document.getElementById('destination-filter');
    const filterCount = document.getElementById('filter-count');
    const rideCards = document.querySelectorAll('.ride-card');

    // Filtering logic
    filterInput.addEventListener('input', () => {
        const query = filterInput.value.toLowerCase().trim();
        let visibleCount = 0;
        let firstMatchLocation = null;

        rideCards.forEach(card => {
            const startName = card.dataset.startName.toLowerCase();
            const endName = card.dataset.endName.toLowerCase();

            if (query === '' || endName.includes(query) || startName.includes(query)) {
                card.classList.remove('hidden');
                visibleCount++;
                if (!firstMatchLocation && endName.includes(query)) {
                    firstMatchLocation = {
                        lat: parseFloat(card.dataset.endLat),
                        lon: parseFloat(card.dataset.endLon),
                        name: card.dataset.endName
                    };
                }
            } else {
                card.classList.add('hidden');
            }
        });

        // Update count display
        if (query !== '') {
            filterCount.textContent = `${visibleCount} trajet(s) correspondant(s)`;
            filterCount.classList.remove('hidden');
        } else {
            filterCount.classList.add('hidden');
        }

        // Add/update destination marker
        if (destinationMarker) {
            map.removeLayer(destinationMarker);
            destinationMarker = null;
        }

        if (query !== '' && firstMatchLocation) {
            destinationMarker = L.marker([firstMatchLocation.lat, firstMatchLocation.lon], {
                icon: L.divIcon({
                    className: 'destination-marker',
                    html: '<div class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-lg shadow-lg whitespace-nowrap">Destination</div>',
                    iconSize: [80, 30],
                    iconAnchor: [40, 30]
                })
            }).addTo(map);
            map.setView([firstMatchLocation.lat, firstMatchLocation.lon], 12);
            placeholder.classList.add('hidden');
        }
    });

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