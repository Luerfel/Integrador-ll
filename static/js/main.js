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
    .then(response => response.text())
    .then(data => {
        if (data.includes('Credenciais inválidas')) {
            alert('Credenciais inválidas');
        } else {
            window.location.href = data;
        }
    })
    .catch(error => console.error('Erro:', error));
});
