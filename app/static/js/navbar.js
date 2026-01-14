document.addEventListener('DOMContentLoaded', () => {
    // Mobile navbar menu toggle
    document.getElementById('mobile-menu-btn')?.addEventListener('click', () => {
        const nav = document.querySelector('header nav');
        const menu = document.getElementById('mobile-menu');
        const hamburger = document.getElementById('hamburger-icon');
        const close = document.getElementById('close-icon');
        menu.classList.toggle('hidden');
        hamburger.classList.toggle('hidden');
        close.classList.toggle('hidden');
        nav.classList.toggle('rounded-full');
        nav.classList.toggle('rounded');
    });
});
