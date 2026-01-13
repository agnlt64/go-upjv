document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([49.8942, 2.2957], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    let routingControl = null;
    let markers = [];
    const placeholder = document.getElementById('map-placeholder');

    document.querySelectorAll('.ride-card').forEach(card => {
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

            document.querySelectorAll('.ride-card').forEach(c => c.classList.remove('ring-2', 'ring-indigo-500'));
            card.classList.add('ring-2', 'ring-indigo-500');
        });
    });

    setTimeout(() => map.invalidateSize(), 200);
});