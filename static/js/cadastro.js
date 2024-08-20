/* 
O arquivo cadastro.js contém o código JavaScript que lida com o envio do formulário de cadastro.
- Ele intercepta o envio do formulário (evento 'submit') para evitar o comportamento padrão de recarregar a página.
- Coleta o valor do campo de email e realiza uma verificação básica para garantir que o email contém "@" e ".".
- Se o email for considerado inválido, uma mensagem de erro genérica "Email digitado é inválido." é exibida.
- Se o email for válido, o formulário é submetido ao servidor Flask para processamento.
- Após o carregamento da página, o script verifica se existe uma mensagem de erro proveniente do backend e, se existir, exibe essa mensagem como um alerta.

Uso: Este script é essencial para validar o formato de email no frontend e garantir uma experiência de usuário consistente.
*/

document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita o envio do formulário para validação imediata

    const email = document.querySelector('input[name="email"]').value; // Coleta o valor do email inserido
    const emailError = document.getElementById('emailError'); // Seleciona o elemento onde a mensagem de erro será exibida

    // Verificação simples para garantir que o email contém "@" e "."
    if (!email.includes('@') || !email.includes('.')) {
        emailError.textContent = 'Email digitado é inválido.'; // Define a mensagem de erro se o email for inválido
        return; // Interrompe o processo de submissão do formulário se o email for inválido
    } else {
        emailError.textContent = ''; // Limpa a mensagem de erro caso o email seja válido
        this.submit(); // Submete o formulário ao servidor Flask para processamento
    }
});

// Após o carregamento da página, verifica se existe uma mensagem de erro proveniente do backend
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cadastroForm'); // Seleciona o formulário de cadastro
    const errorMessage = form.getAttribute('data-error-message'); // Coleta a mensagem de erro do atributo data-error-message
    if (errorMessage) {
        alert(errorMessage); // Exibe a mensagem de erro como um alerta se existir
    }
});
