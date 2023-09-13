document.querySelector('form').addEventListener('submit', function(event) {
    var form = document.getElementById('form-login');
    form.classList.add('was-validated');
    form.setAttribute('novalidate', '');
    
    var usernameInput = document.getElementById("yourUsername");
    var passwordInput = document.getElementById("yourPassword");

    if (usernameInput.checkValidity() === false) {
        usernameInput.classList.add("is-invalid");
        event.preventDefault();
    } else {
        usernameInput.classList.remove("is-invalid");
    }

    if (passwordInput.checkValidity() === false) {
        passwordInput.classList.add("is-invalid");
        event.preventDefault();
    } else {
        passwordInput.classList.remove("is-invalid");
    }
});

function showPassword() {
    const passwordInput = document.getElementById('yourPassword');
    const showHideButton = document.getElementById('show-hide-password');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
 
}
