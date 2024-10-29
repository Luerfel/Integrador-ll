// Função principal para lidar com ações de eventos (aprovação/reprovação)
function handleEventAction(eventId, action) {
    /* Envia uma ação relacionada a um evento para o servidor e processa a resposta */
    // Inicia uma requisição POST usando fetch para enviar dados ao servidor
    fetch('/acao_evento', {
        method: 'POST', // Define o método HTTP como POST
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Define o tipo de conteúdo da requisição
        },
        body: `evento_id=${eventId}&acao=${action}` // Define o corpo da requisição com os parâmetros do evento e da ação
    })
    .then(response => {
        if (response.ok) { // Verifica se a resposta do servidor foi bem-sucedida (status HTTP 200)
            // Seleciona o elemento HTML correspondente ao evento para remoção da lista
            const eventRow = document.getElementById(`event-${eventId}`);
            if (eventRow) {
                eventRow.remove(); // Remove o evento da lista se o elemento existir no DOM
            }
        } else {
            // Exibe uma mensagem de erro se a resposta do servidor não for bem-sucedida
            alert('Ocorreu um erro ao processar a ação. Tente novamente.');
        }
    })
    .catch(() => {
        // Lida com erros de rede ou qualquer outro problema na requisição
        alert('Ocorreu um erro ao processar a ação. Tente novamente.');
    });
}

// Função para abrir o modal de justificativa de reprovação
function abrirModalReprovar(eventoId) {
    // Seleciona o elemento modal no DOM
    const modal = document.getElementById('modalReprovar');
    // Define o campo oculto no modal com o ID do evento para referência posterior
    const eventoIdInput = document.getElementById('modalEventoId');
    
    eventoIdInput.value = eventoId; // Atribui o ID do evento ao campo oculto do modal
    modal.style.display = 'block'; // Torna o modal visível
}

// Função para fechar o modal de justificativa de reprovação
function fecharModalReprovar() {
    const modal = document.getElementById('modalReprovar'); // Seleciona o modal
    modal.style.display = 'none'; // Oculta o modal
}

// Fecha o modal se o usuário clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modalReprovar'); // Seleciona o modal
    if (event.target === modal) { // Verifica se o clique foi fora do modal
        modal.style.display = 'none'; // Fecha o modal
    }
}

// Fecha o modal ao clicar no botão de fechar (X)
document.querySelector('.close').onclick = fecharModalReprovar; // Associa o clique no botão de fechar à função de fechar o modal

// Lida com o envio do formulário de reprovação e remove o evento da lista
document.getElementById('formReprovarEvento').onsubmit = function(event) {
    event.preventDefault(); // Previne o comportamento padrão de envio do formulário
    const eventoId = document.getElementById('modalEventoId').value; // Obtém o ID do evento do campo oculto no modal

    const formData = new FormData(this); // Cria um objeto FormData com os dados do formulário
    
    // Envia uma requisição POST para o servidor com os dados do formulário
    fetch('/acao_evento', {
        method: 'POST', // Define o método como POST
        body: new URLSearchParams(formData) // Converte os dados do formulário para URLSearchParams e define como corpo da requisição
    }).then(response => {
        if (response.ok) { // Verifica se a resposta do servidor foi bem-sucedida
            document.getElementById(`event-${eventoId}`).remove(); // Remove o evento da lista
            fecharModalReprovar(); // Fecha o modal após o envio bem-sucedido
        } else {
            alert('Erro ao reprovar o evento.'); // Exibe mensagem de erro em caso de falha
        }
    }).catch(error => {
        alert('Erro ao reprovar o evento.'); // Trata qualquer erro na requisição
    });
};
