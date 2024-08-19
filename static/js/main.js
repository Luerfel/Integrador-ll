// main.js

// Funções a serem adicionadas futuramente para o botão "Entrar" e "Novo aqui? Crie uma conta"
document.querySelector('button').addEventListener('click', function() {
    alert('Botão Entrar clicado!');
});

document.querySelector('.signup-link a').addEventListener('click', function(event) {
    event.preventDefault();
    alert('Link para criar conta clicado!');
});
