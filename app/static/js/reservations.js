(function () {

  function createPassengersModal() {
    const modal = document.createElement('div');
    modal.className = 'passengers-modal fixed inset-0 z-50 flex items-center justify-center p-4';
    modal.innerHTML = `
      <div class="modal-overlay absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
      <div class="modal-content relative bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all">
        
        <header class="bg-indigo-600 p-4 flex items-center justify-between">
          <h3 class="text-lg font-bold text-white flex items-center gap-2">
            Passagers inscrits
          </h3>
          <button class="modal-close text-indigo-100 hover:text-white transition">✕</button>
        </header>

        <div class="p-4 bg-slate-50 min-h-[150px] max-h-[60vh] overflow-y-auto passenger-list">
           </div>

        <div class="p-4 border-t border-slate-200 bg-white flex justify-end">
          <button class="modal-close px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition text-sm">
            Fermer
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    return modal;
  }

  function openPassengersModal(rideId) {
    const modal = createPassengersModal();
    const listEl = modal.querySelector('.passenger-list');
    
    const close = () => { modal.remove(); document.removeEventListener('keydown', onEsc); };
    const onEsc = (e) => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', onEsc);
    modal.querySelectorAll('.modal-close').forEach(btn => btn.addEventListener('click', close));

    // Chargement
    listEl.innerHTML = `
        <div class="flex flex-col items-center justify-center h-32 text-indigo-500 gap-3">
            <div class="animate-spin h-8 w-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full"></div>
            <span class="text-sm font-medium text-slate-500">Récupération des données...</span>
        </div>`;

    fetch(`/rides/${rideId}/passengers`)
      .then(resp => {
        if (!resp.ok) throw new Error('Erreur réseau');
        return resp.json();
      })
      .then(data => {
        const passengers = data.passengers || [];

        if (passengers.length === 0) {
          listEl.innerHTML = `
            <div class="flex flex-col items-center justify-center h-32 text-slate-400">
                <p class="text-sm italic">Aucun passager inscrit.</p>
            </div>`;
          return;
        }

        const ul = document.createElement('ul');
        ul.className = 'space-y-3';

        passengers.forEach(p => {
          const li = document.createElement('li');
          li.className = 'bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between';
          
          const safeName = escapeHtml(p.name);
          const safeId = escapeHtml(p.upjv_id); // Affiche l'ID étudiant (ex: g22303303)

          li.innerHTML = `
            <div class="flex items-center gap-3">
                 <div class="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-lg border border-indigo-200 shrink-0">
                    ${p.avatar_initial}
                 </div>
                 <div class="flex flex-col">
                    <span class="font-semibold text-slate-800">${safeName}</span>
                    <span class="text-xs text-slate-500 font-mono">ID: ${safeId}</span>
                 </div>
            </div>
          `;
          ul.appendChild(li);
        });

        listEl.innerHTML = '';
        listEl.appendChild(ul);
      })
      .catch(err => {
        console.error(err);
        listEl.innerHTML = '<div class="text-center text-red-500 py-6">Erreur de chargement.</div>';
      });
  }

  function escapeHtml(text) {
    if (!text) return "";
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function init() {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('.btn-view-passengers');
      if (btn && btn.dataset.rideId) {
        openPassengersModal(btn.dataset.rideId);
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();

})();