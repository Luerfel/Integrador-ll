// Simples animação de transição ao clicar no link "Criar conta"
document.querySelector('.signup-link a').addEventListener('click', function(event) {
    event.preventDefault();
    
    // Adiciona a classe shrink para iniciar a animação
    document.querySelector('.login-container').classList.add('shrink');
    
    // Espera 0.5 segundos (a duração da animação) antes de redirecionar
    setTimeout(function() {
        window.location.href = 'cadastro';
    }, 500);
});
