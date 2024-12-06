function toggleDropdown(event) {
    const menu = event.currentTarget.nextElementSibling; // Seleciona o próximo elemento (o menu)
    const isOpen = menu.style.display === 'block';

    // Oculta todos os outros menus
    const allMenus = document.querySelectorAll('.dropdown-menu');
    allMenus.forEach(m => m.style.display = 'none');

    // Alterna a visibilidade do menu clicado
    menu.style.display = isOpen ? 'none' : 'block';

    // Previne a propagação do clique
    event.stopPropagation();
}

document.addEventListener('click', function() {
    const menus = document.querySelectorAll('.dropdown-menu');
    menus.forEach(menu => menu.style.display = 'none'); // Fecha o menu ao clicar fora
});
