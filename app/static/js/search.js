document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([49.8942, 2.2957], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    let routingControl = null;
    let routeMarkers = [];
    let destinationMarker = null;

    setTimeout(() => { map.invalidateSize(); }, 200);
    loadRides(null, null);

    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('change', async function(e) {
        const query = e.target.value;
        if (query.length > 3) {
            try {
                const response = await fetch(`https://api-adresse.data.gouv.fr/search/?q=${query}&limit=1`);
                const data = await response.json();
                if (data.features && data.features.length > 0) {
                    const [lon, lat] = data.features[0].geometry.coordinates;
                    map.setView([lat, lon], 14);
                    if (destinationMarker) map.removeLayer(destinationMarker);
                    destinationMarker = L.marker([lat, lon]).addTo(map).bindPopup("Destination").openPopup();
                    loadRides(lat, lon);
                }
            } catch (err) { console.error(err); }
        }
    });

    function loadRides(lat, lon) {
        let url = '/api/search-rides';
        if (lat && lon) url += `?lat=${lat}&lon=${lon}`;

        fetch(url)
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('rides-container');
                container.innerHTML = '';
                if (data.success && data.rides.length > 0) {
                    data.rides.forEach(ride => {
                        const div = document.createElement('article');
                        div.className = "bg-[oklch(96.7%_0.003_264.542)] shadow-md rounded-lg p-4 mb-6 transition-all duration-200 relative hover:shadow-lg cursor-pointer";
                        let distanceHtml = ride.distance > 0 ? `<span class="absolute top-2 right-2 text-[10px] font-bold text-green-600 bg-green-100 px-2 py-1 rounded-full">${ride.distance.toFixed(1)} km</span>` : '';

                        // BOUTON ACTIF (appelle bookRide)
                        div.innerHTML = `
                            ${distanceHtml}
                            <div class="md:flex md:items-center gap-4" onclick="showRoute(${ride.start_lat}, ${ride.start_lon}, ${ride.end_lat}, ${ride.end_lon})">
                                <div class="flex items-center justify-center w-20 h-20 bg-indigo-50 text-indigo-700 rounded-lg flex-col shrink-0">
                                    <span class="text-xs font-bold uppercase">${ride.date_month}</span>
                                    <span class="text-2xl font-bold">${ride.date_day}</span>
                                    <span class="text-xs">${ride.date_year}</span>
                                </div>
                                <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-3 px-2 mt-4 md:mt-0">
                                    <div><div class="text-sm text-slate-500">Chauffeur</div><div class="font-medium text-slate-900">${ride.driver_name}</div></div>
                                    <div><div class="text-sm text-slate-500">Places</div><div class="font-medium text-slate-900">${ride.seats} libre(s)</div></div>
                                    <div><div class="text-sm text-slate-500">Départ</div><div class="font-medium text-slate-900 leading-tight">${ride.departure}</div></div>
                                    <div><div class="text-sm text-slate-500">Arrivée</div><div class="font-medium text-slate-900 leading-tight">${ride.arrival}</div></div>
                                </div>
                                <div class="flex flex-col items-end gap-2 mt-4 md:mt-0">
                                    <button onclick="event.stopPropagation(); bookRide(${ride.id}, this)" class="bg-indigo-600 text-white font-medium px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors shadow-sm text-sm whitespace-nowrap">Réserver</button>
                                </div>
                            </div>
                        `;
                        container.appendChild(div);
                    });
                } else { container.innerHTML = '<p class="text-center py-10 text-gray-500">Aucun trajet trouvé.</p>'; }
            });
    }

    window.showRoute = function(lat1, lon1, lat2, lon2) {
        if (routingControl) { map.removeControl(routingControl); routingControl = null; }
        routeMarkers.forEach(m => map.removeLayer(m));
        routeMarkers = [];
        if(lat1 && lon1 && lat2 && lon2) {
            routingControl = L.Routing.control({
                waypoints: [L.latLng(lat1, lon1), L.latLng(lat2, lon2)],
                routeWhileDragging: false,
                lineOptions: { styles: [{color: '#4f46e5', weight: 6}] },
                createMarker: () => null 
            }).addTo(map);
            let m1 = L.marker([lat1, lon1]).addTo(map).bindPopup("Départ");
            let m2 = L.marker([lat2, lon2]).addTo(map).bindPopup("Arrivée");
            routeMarkers.push(m1, m2);
        }
    };

    // FONCTION RESERVATION
    window.bookRide = function(rideId, btn) {
        btn.innerText = "...";
        btn.disabled = true;
        fetch(`/api/book-ride/${rideId}`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    btn.className = "bg-green-600 text-white font-medium px-4 py-2 rounded-md shadow-sm text-sm whitespace-nowrap";
                    btn.innerText = "Réservé !";
                    setTimeout(() => location.reload(), 1500);
                } else {
                    alert(data.message);
                    btn.innerText = "Erreur";
                    btn.className = "bg-red-500 text-white font-medium px-4 py-2 rounded-md shadow-sm text-sm";
                    btn.disabled = false;
                }
            })
            .catch(err => { console.error(err); btn.innerText = "Erreur"; });
    };
});