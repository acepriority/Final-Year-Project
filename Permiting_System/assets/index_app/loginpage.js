document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', () => {
        const passwordField = button.previousElementSibling;
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        button.innerHTML = type === 'password' ? '<i class="fa fa-eye"></i>' : '<i class="fa fa-eye-slash"></i>';
    });
});