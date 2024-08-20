// Função para redirecionar o usuário após o login
function redirectUser(event) {
    // Previne o comportamento padrão do formulário (recarregar a página)
    event.preventDefault();
    
    // Obtém os valores dos campos de email e senha
    const email = document.querySelector('input[name="email"]').value;
    const senha = document.querySelector('input[name="senha"]').value;
    
    // Redireciona para a rota de login com as credenciais na URL
    window.location.href = `/login/${email}/${senha}`;
}

// Adiciona um listener para o evento de submissão do formulário
document.getElementById('loginForm').addEventListener('submit', redirectUser);
