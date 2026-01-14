document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[name="delete-review"]').forEach(button => {
        button.addEventListener('click', async function () {
            const reviewId = this.dataset.reviewId;
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet avis ?')) return;

            try {
                const response = await fetch(`/api/reviews/${reviewId}`, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' }
                });

                if (response.ok) {
                    location.reload();
                } else {
                    alert('Erreur lors de la suppression de l\'avis');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Erreur lors de la suppression de l\'avis');
            }
        });
    });
});
