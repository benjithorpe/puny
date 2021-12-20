const navbarToggle = document.querySelector('.uk-navbar-toggle');
navbarToggle.addEventListener('click', () => {
  document.querySelector('nav ul').classList.toggle('uk-flex');
});
