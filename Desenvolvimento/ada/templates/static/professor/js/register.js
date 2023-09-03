document.querySelector('form').addEventListener('submit', function(event) {
    var form = document.getElementById('form-login');
    form.classList.add('was-validated');
    form.setAttribute('novalidate', '');

    var emailInput = document.getElementById("yourEmail");
    var passwordInput = document.getElementById("yourPassword");

    if (emailInput.checkValidity() === false) {
        emailInput.classList.add("is-invalid");
        event.preventDefault();
    } else {
        emailInput.classList.remove("is-invalid");
    }

    if (passwordInput.checkValidity() === false) {
        passwordInput.classList.add("is-invalid");
        event.preventDefault();
    } else {
        passwordInput.classList.remove("is-invalid");
    }
});
