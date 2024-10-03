/* 
O arquivo cadastro.js contém o código JavaScript que lida com o envio do formulário de cadastro.
- Ele intercepta o envio do formulário (evento 'submit') para evitar o comportamento padrão de recarregar a página.
- Coleta o valor do campo de email e realiza uma verificação básica para garantir que o email contém "@" e ".".
- Se o email for considerado inválido, uma mensagem de erro genérica "Email digitado é inválido." é exibida.
- Se o email for válido, o formulário é submetido ao servidor Flask para processamento.
- Após o carregamento da página, o script verifica se existe uma mensagem de erro proveniente do backend e, se existir, exibe essa mensagem como um alerta.

Uso: Este script é essencial para validar o formato de email no frontend e garantir uma experiência de usuário consistente.
*/

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio automático do formulário

    const email = document.querySelector('input[name="email"]').value; // Pega o valor do campo de email

    // Validação simples de email
    if (!email.includes('@') || !email.includes('.')) {
        alert('Email inválido. Por favor, insira um email válido.');
        return; // Impede o envio se o email for inválido
    }

    // Coleta os dados do formulário
    const formData = new FormData(this);

    // Envia o formulário usando fetch para evitar recarregamento da página
    fetch('/cadastro', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            // Cadastro realizado com sucesso, exibe a pergunta sobre adicionar créditos
            const addCredits = confirm("Deseja adicionar créditos à sua carteira?");
            
            // Redireciona de acordo com a escolha do usuário
            if (addCredits) {
                window.location.href = "/gerenciar_carteira";
            } else {
                window.location.href = "/area_usuario";
            }
        } else {
            // Se houver erro no cadastro
            alert('Erro ao realizar o cadastro. Tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro. Por favor, tente novamente mais tarde.');
    });
});
