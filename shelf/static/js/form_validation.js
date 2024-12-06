document.addEventListener('DOMContentLoaded', function () {
    var form  = document.getElementById('contactForm');

    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()){
            event.preventDefault();
            event.stopPropagation()
        }
        form.classList.add('was-valitaded');
    }, false);
});