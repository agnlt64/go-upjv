document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('review-modal');
    const form = document.getElementById('review-form');
    const cancelBtn = document.getElementById('cancel-review');
    const starBtns = document.querySelectorAll('.star-btn');
    const ratingInput = document.getElementById('review-rating');

    let selectedRating = 0;

    document.querySelectorAll('.btn-review').forEach(btn => {
        btn.addEventListener('click', () => {
            const rideId = btn.dataset.rideId;
            const driverId = btn.dataset.driverId;
            const driverName = btn.dataset.driverName;

            document.getElementById('review-ride-id').value = rideId;
            document.getElementById('review-target-id').value = driverId;
            document.getElementById('review-driver-name').textContent = `Conducteur : ${driverName}`;

            resetStars();
            document.getElementById('review-content').value = '';
            modal.classList.remove('hidden');
        });
    });

    starBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            selectedRating = parseInt(btn.dataset.value);
            ratingInput.value = selectedRating;
            updateStars(selectedRating);
        });
    });

    function updateStars(rating) {
        starBtns.forEach(btn => {
            const value = parseInt(btn.dataset.value);
            btn.classList.toggle('text-yellow-400', value <= rating);
            btn.classList.toggle('text-gray-300', value > rating);
        });
    }

    function resetStars() {
        selectedRating = 0;
        ratingInput.value = '';
        starBtns.forEach(btn => {
            btn.classList.remove('text-yellow-400');
            btn.classList.add('text-gray-300');
        });
    }

    cancelBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!selectedRating) {
            alert('Veuillez sélectionner une note');
            return;
        }

        const data = {
            ride_id: parseInt(document.getElementById('review-ride-id').value),
            target_id: parseInt(document.getElementById('review-target-id').value),
            rating: selectedRating,
            content: document.getElementById('review-content').value
        };

        try {
            const response = await fetch('/api/submit-review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                modal.classList.add('hidden');
                window.location.reload();
            } else {
                alert(result.message || 'Une erreur est survenue');
            }
        } catch (err) {
            alert('Erreur de connexion');
        }
    });
});
