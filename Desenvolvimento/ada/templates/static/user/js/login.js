document.querySelector('form').addEventListener('submit', function(event) {
    var form = document.getElementById('form-login');
    form.classList.add('was-validated');
    form.setAttribute('novalidate', '');
    
    var usernameInput = document.getElementById("yourUsername");
    var passwordInput = document.getElementById("yourPassword");
    
     /* Validação de user
    var username = yourUsername.value;
    var password = yourPassword.value;
    if (username === 'sp1' && password === 'ada') {
        this.submit();
    } else {
        document.getElementById('loginError').style.display = 'block';
        document.getElementById("yourUsername").value = "";
        document.getElementById("yourPassword").value = "";
        document.getElementById('passwordError').style.display = 'none';
        document.getElementById('usernameError').style.display = 'none';
    }
    */

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
