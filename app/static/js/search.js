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

    // --- RECHERCHE ADRESSE ---
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

                        div.innerHTML = `
                            ${distanceHtml}
                            <div class="md:flex md:items-center gap-4">
                                <div class="flex items-center justify-center w-20 h-20 bg-indigo-50 text-indigo-700 rounded-lg flex-col shrink-0">
                                    <span class="text-xs font-bold uppercase">${ride.date_month}</span>
                                    <span class="text-2xl font-bold">${ride.date_day}</span>
                                    <span class="text-xs">${ride.date_year}</span>
                                </div>
                                <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-3 px-2 mt-4 md:mt-0">
                                    <div><div class="text-sm text-slate-500">Chauffeur</div><div class="font-medium text-slate-900">${ride.driver_name}</div></div>
                                    <div><div class="text-sm text-slate-500">Places</div><div class="font-medium text-slate-900">${ride.seats} libre(s)</div></div>
                                    <div><div class="text-sm text-slate-500">Départ</div><div class="font-medium text-slate-900 leading-tight">${ride.departure}<span class="block text-xs text-slate-600 mt-1">${ride.time_start}</span></div></div>
                                    <div><div class="text-sm text-slate-500">Arrivée</div><div class="font-medium text-slate-900 leading-tight">${ride.arrival}<span class="block text-xs text-slate-600 mt-1">${ride.time_end}</span></div></div>
                                </div>
                                <div class="flex flex-col items-end gap-2 mt-4 md:mt-0">
                                    <button onclick="alert('Bientôt disponible')" class="bg-gray-400 text-white font-medium px-4 py-2 rounded-md shadow-sm text-sm whitespace-nowrap">Réserver</button>
                                </div>
                            </div>
                        `;
                        container.appendChild(div);
                    });
                } else {
                    container.innerHTML = '<p class="text-sm text-slate-500 italic text-center py-10">Aucun trajet disponible.</p>';
                }
            });
    }
});