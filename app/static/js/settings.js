
const editProfileBtn = document.getElementById('editProfileBtn');
const cancelProfileBtn = document.getElementById('cancelProfileBtn');
const profileForm = document.getElementById('profileForm');
const profileActions = document.getElementById('profileActions');
const profileInputs = profileForm.querySelectorAll('input:not([type="hidden"])');
const bioInput = profileForm.querySelector('textarea[name="bio"]');

editProfileBtn.addEventListener('click', () => {
    profileInputs.forEach(input => input.disabled = false);
    bioInput.disabled = false;
    profileActions.classList.remove('hidden');
    editProfileBtn.classList.add('hidden');
});

cancelProfileBtn.addEventListener('click', () => {
    profileForm.reset();
    profileInputs.forEach(input => input.disabled = true);
    bioInput.disabled = true;
    profileActions.classList.add('hidden');
    editProfileBtn.classList.remove('hidden');
});


const editVehicleBtn = document.getElementById('editVehicleBtn');
const cancelVehicleBtn = document.getElementById('cancelVehicleBtn');
const vehicleDisplay = document.getElementById('vehicleDisplay');
const vehicleForm = document.getElementById('vehicleForm');

try {
    editVehicleBtn.addEventListener('click', () => {
        vehicleDisplay.classList.add('hidden');
        vehicleForm.classList.remove('hidden');
        editVehicleBtn.classList.add('hidden');
    });
    
    cancelVehicleBtn.addEventListener('click', () => {
        vehicleForm.reset();
        vehicleDisplay.classList.remove('hidden');
        vehicleForm.classList.add('hidden');
        editVehicleBtn.classList.remove('hidden');
    });
    
    // Gestion de la suppression du véhicule
    const deleteVehicleBtn = document.getElementById('deleteVehicleBtn');
    deleteVehicleBtn.addEventListener('click', () => {
        // todo: fetch le backend pour supprimer le véhicule
    });
} catch (e) {
    // pas de véhicule, pas d'erreur
}

try {
    // Gestion de l'ajout de véhicule
    const addVehicleBtn = document.getElementById('addVehicleBtn');
    const cancelAddVehicleBtn = document.getElementById('cancelAddVehicleBtn');
    const noVehicle = document.getElementById('noVehicle');
    const addVehicleForm = document.getElementById('addVehicleForm');
    
    addVehicleBtn.addEventListener('click', () => {
        noVehicle.classList.add('hidden');
        addVehicleForm.classList.remove('hidden');
    });
    
    cancelAddVehicleBtn.addEventListener('click', () => {
        addVehicleForm.reset();
        noVehicle.classList.remove('hidden');
        addVehicleForm.classList.add('hidden');
    });
} catch(e) {
    // déjà un véhicule, pas d'erreur
}


// Gestion du changement de mot de passe
const changePasswordBtn = document.getElementById('changePasswordBtn');
const cancelPasswordBtn = document.getElementById('cancelPasswordBtn');
const passwordDisplay = document.getElementById('passwordDisplay');
const passwordForm = document.getElementById('passwordForm');

changePasswordBtn.addEventListener('click', () => {
    passwordDisplay.classList.add('hidden');
    passwordForm.classList.remove('hidden');
    changePasswordBtn.classList.add('hidden');
});

cancelPasswordBtn.addEventListener('click', () => {
    passwordForm.reset();
    passwordDisplay.classList.remove('hidden');
    passwordForm.classList.add('hidden');
    changePasswordBtn.classList.remove('hidden');
});