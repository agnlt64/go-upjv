document.addEventListener('DOMContentLoaded', function() {
    
    // On écoute les clics sur toute la page
    document.body.addEventListener('click', function(e) {
        
        // On vérifie si on a cliqué sur un bouton "Passagers"
        const button = e.target.closest('.btn-toggle-passengers');
        
        if (button) {
            // On récupère l'ID du trajet (ex: 12)
            const rideId = button.dataset.rideId;
            // On cible la liste cachée correspondante (passenger-list-12)
            const listDiv = document.getElementById(`passenger-list-${rideId}`);
            
            if (listDiv) {
                // On bascule l'affichage (montrer/cacher)
                listDiv.classList.toggle('hidden');
            }
        }
    });

});