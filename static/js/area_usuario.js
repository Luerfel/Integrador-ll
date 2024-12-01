function openModal(eventoId, eventoNome, aposta) {
    // Preencher os dados do modal com as informações do evento
    document.getElementById('modal-evento-nome').innerText = `Apostar em ${eventoNome}`;
    document.getElementById('modal-evento-id').value = eventoId;
    document.getElementById('modal-aposta').value = aposta;

    // Exibir o modal
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    // Ocultar o modal
    document.getElementById('modal').style.display = 'none';
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
    document.getElementById('form-aposta').submit();
});
