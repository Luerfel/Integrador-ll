function openMenu() {
    document.getElementById("sideMenu").style.width = "250px";
}

function closeMenu() {
    document.getElementById("sideMenu").style.width = "0";
}
document.getElementById('apostar-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Previne o comportamento padrão

    // Seleciona os campos do formulário
    const valorApostaInput = document.getElementById('valor_aposta');
    const valorAposta = parseFloat(valorApostaInput.value);
    const erroMensagem = document.getElementById('erro-mensagem'); // Elemento para exibir mensagens de erro

    // Limpa mensagens de erro anteriores
    erroMensagem.textContent = '';

    // Validação do valor da aposta
    if (isNaN(valorAposta) || valorAposta <= 0) {
        erroMensagem.textContent = 'Por favor, insira um valor de aposta válido.';
        return; // Impede o envio do formulário
    }

    // Se a validação passar, submete o formulário manualmente
    document.getElementById('apostar-form').submit();
});

document.getElementById('form-aposta').addEventListener('submit', function(e) {
    e.preventDefault();  // Previne o envio normal do formulário

    // Obtém os dados do formulário
    const formData = new FormData(this);

    // Faz a requisição AJAX
    fetch('/apostar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Aqui você pode abrir a janela de sucesso
            alert(data.message);  // Ou outra lógica para abrir a janela
        } else {
            alert(data.message);  // Exibe a mensagem de erro
        }
    })
    .catch(error => console.error('Erro:', error));
});
