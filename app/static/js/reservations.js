document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', (e) => {
        const button = e.target.closest('.btn-toggle-passengers');
        
        if (button) {
            const rideId = button.dataset.rideId;
            const listDiv = document.getElementById(`passenger-list-${rideId}`);
            
            if (listDiv) {
                listDiv.classList.toggle('hidden');
            }
        }
    });
});