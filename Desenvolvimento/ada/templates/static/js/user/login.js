document.querySelector('#submitBtn').addEventListener('click', function() {
    event.preventDefault();
    event.stopPropagation();
    
    var form = document.getElementById('form-login');
    form.classList.add('was-validated');
    form.setAttribute('novalidate', '');
    
    var usernameInput = document.getElementById("yourUsername");
    var passwordInput = document.getElementById("yourPassword");

    if (usernameInput.checkValidity() === false) {
        usernameInput.classList.add("is-invalid");
    } else {
        usernameInput.classList.remove("is-invalid");
    }

    if (passwordInput.checkValidity() === false) {
        passwordInput.classList.add("is-invalid");
    } else {
        passwordInput.classList.remove("is-invalid");
    }
});

document.getElementById("yourUsername").addEventListener('input', function() {
    this.classList.remove("is-invalid");
});

document.getElementById("yourPassword").addEventListener('input', function() {
    this.classList.remove("is-invalid");
});