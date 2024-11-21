const menuButton = document.getElementById('menu-button');
const sidebar = document.getElementById('sidebar');

menuButton.addEventListener('click', () => {
  if (sidebar.style.left === '0px') {
    sidebar.style.left = '-250px'; // Fecha o menu
  } else {
    sidebar.style.left = '0px'; // Abre o menu
  }
});