async function toggleUserStatus(userId) {
    try {
        const response = await fetch(`/api/toggle-user/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Reload the page to reflect changes
            location.reload();
        } else {
            alert('Erreur lors de la modification du statut');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la modification du statut');
    }
}

async function toggleAdminRole(userId) {
    try {
        const response = await fetch(`/api/toggle-admin/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Reload the page to reflect changes
            location.reload();
        } else {
            alert('Erreur lors de la modification du rôle');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la modification du rôle');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('button[name="toggle-user"]');
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.getAttribute('data-user-id');
            toggleUserStatus(userId);
        });
    });

    const toggleAdminButtons = document.querySelectorAll('button[name="toggle-admin"]');
    toggleAdminButtons.forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.getAttribute('data-user-id');
            toggleAdminRole(userId);
        });
    });
});