
/* O arquivo main.js contém o código JavaScript que lida com o envio do formulário de login.
- Ele intercepta o envio do formulário (evento 'submit') para evitar o comportamento padrão de recarregar a página.
- Coleta os valores de email e senha dos campos de entrada.
- Envia uma requisição POST para a rota '/', onde os dados são processados no servidor Flask.
- Se as credenciais forem inválidas, uma mensagem de erro é exibida como uma notificação (via alert()).
- Se as credenciais forem válidas, o usuário é redirecionado para a página apropriada (área do usuário ou moderador).

Uso: Este script é essencial para o funcionamento da interface de login, manipulando a interação do usuário de forma dinâmica.
*/

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Evita o comportamento padrão do formulário (recarregar a página)

    // Coletar os dados do formulário
    const email = document.querySelector('input[name="email"]').value;
    const senha = document.querySelector('input[name="senha"]').value;

    // Enviar a requisição via POST para o servidor
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${encodeURIComponent(email)}&senha=${encodeURIComponent(senha)}`
    })
    .then(response => {
        // Verifica se a resposta é 401 (não autorizado)
        if (response.status === 401) {
            return response.text().then(text => {
                // Exibe a notificação de erro
                alert(text);  // Exibe a mensagem de erro como uma notificação
                return Promise.reject('Credenciais inválidas');
            });
        }
        return response.text();  // Recebe a URL de redirecionamento como texto
    })
    .then(url => {
        console.log('Redirecionando para:', url);
        window.location.href = url;  // Redireciona para a URL recebida do servidor
    })
    .catch(error => console.error('Erro:', error));  // Loga o erro caso ocorra
});
