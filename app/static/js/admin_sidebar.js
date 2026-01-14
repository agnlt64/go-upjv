document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('admin-sidebar');
    const overlay = document.getElementById('admin-sidebar-overlay');
    const toggle = document.getElementById('admin-sidebar-toggle');
    const openIcon = document.getElementById('admin-sidebar-open');
    const closeIcon = document.getElementById('admin-sidebar-close');

    const toggleSidebar = () => {
        sidebar?.classList.toggle('-translate-x-full');
        overlay?.classList.toggle('hidden');
        openIcon?.classList.toggle('hidden');
        closeIcon?.classList.toggle('hidden');
    };

    toggle?.addEventListener('click', toggleSidebar);
    overlay?.addEventListener('click', toggleSidebar);
});
