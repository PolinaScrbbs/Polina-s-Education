document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.header__link');
    const statuses = document.querySelectorAll('.practice__status');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault(); 

            links.forEach(l => l.classList.remove('active-link'));

            this.classList.add('active-link');
        });
    });

    statuses.forEach(status => {
        status.addEventListener('click', function (e) {
            e.preventDefault(); 

            statuses.forEach(l => l.classList.remove('active-status'));

            this.classList.add('active-status');
        });
    });
});
