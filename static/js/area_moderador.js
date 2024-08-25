function handleEventAction(eventId, action) {
    /* é usada para enviar uma ação relacionada a um evento para o servidor,
    processar a resposta do servidor, e atualizar a interface do usuário
    removendo o evento da lista se a ação foi realizada com sucesso.
    Caso haja um erro durante o processo, a função notifica o usuário. */
    // Envia a requisição POST utilizando fetch
    fetch('/acao_evento', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `evento_id=${eventId}&acao=${action}`
    })
    .then(response => {
        if (response.ok) { // Verifica se a resposta foi bem-sucedida (status 200-299)
            // Remove o evento da lista após a ação ser bem-sucedida
            const eventRow = document.getElementById(`event-${eventId}`);
            if (eventRow) {
                eventRow.remove();
            }
        } else {
            // Exibe uma mensagem de erro se a requisição falhar
            alert('Ocorreu um erro ao processar a ação. Tente novamente.');
        }
    })
    .catch(() => {
        // Trata qualquer erro de rede ou outro erro ao processar a requisição
        alert('Ocorreu um erro ao processar a ação. Tente novamente.');
    });
}
// Abrir o modal para justificar a reprovação
function abrirModalReprovar(eventoId) {
    const modal = document.getElementById('modalReprovar');
    const eventoIdInput = document.getElementById('modalEventoId');
    
    eventoIdInput.value = eventoId;
    modal.style.display = 'block';
}

// Fechar o modal
function fecharModalReprovar() {
    const modal = document.getElementById('modalReprovar');
    modal.style.display = 'none';
}

// Fechar o modal ao clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modalReprovar');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Fechar o modal ao clicar no botão de fechar
document.querySelector('.close').onclick = fecharModalReprovar;

// Submeter o formulário e remover o evento da tabela
document.getElementById('formReprovarEvento').onsubmit = function(event) {
    event.preventDefault();
    const eventoId = document.getElementById('modalEventoId').value;

    const formData = new FormData(this);
    
    fetch('/acao_evento', {
        method: 'POST',
        body: new URLSearchParams(formData)
    }).then(response => {
        if (response.ok) {
            document.getElementById(`event-${eventoId}`).remove();
            fecharModalReprovar();
        } else {
            alert('Erro ao reprovar o evento.');
        }
    }).catch(error => {
        alert('Erro ao reprovar o evento.');
    });
};
