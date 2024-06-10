// script.js

document.addEventListener('DOMContentLoaded', function () {
    const togglePasswordButton = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('#password');

    togglePasswordButton.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? '👁️' : '🙈';
    });
});
