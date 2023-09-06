document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const messageInput = document.querySelector('[name="message"]');

    form.addEventListener('submit', function (event) {
        if (!validateMessage()) {
            event.preventDefault();
        }
    });

    messageInput.addEventListener('input', function () {
        validateMessage();
    });

    function validateMessage() {
        const messageValue = messageInput.value;

        if (messageValue.length < 10 || messageValue.length > 300) {
            const messageError = document.querySelector('#messageError');
            messageError.textContent = 'A mensagem deve ter entre 10 e 300 caracteres.';
            messageError.style.color = 'red';
            messageError.style.display = 'block';
            return false;
        } else {
            const messageError = document.querySelector('#messageError');
            messageError.style.display = 'none';
            return true;
        }
    }
});

