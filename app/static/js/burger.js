document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const menu = document.querySelector('.header__menu');
    const closeButton = document.querySelector('.burger__close');

    burger.addEventListener('click', () => {
        burger.classList.toggle('active');
        menu.classList.add('active');
    });

    closeButton.addEventListener('click', () => {
        burger.classList.remove('active');
        menu.classList.remove('active');
    });
});      