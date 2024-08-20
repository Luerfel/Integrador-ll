document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Evita o comportamento padrão do formulário

    // Coletar os dados do formulário
    const email = document.querySelector('input[name="email"]').value;
    const senha = document.querySelector('input[name="senha"]').value;

    // Enviar a requisição via POST
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
        return response.text();
    })
    .then(url => {
        console.log('Redirecionando para:', url);
        window.location.href = url;  // Redireciona para a URL recebida do servidor
    })
    .catch(error => console.error('Erro:', error));
});
