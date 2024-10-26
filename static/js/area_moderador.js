// Função para manipular as ações dos eventos
function handleEventAction(eventoId, acao) {
    // Cria um objeto FormData para enviar os dados via POST
    const formData = new FormData();
    formData.append('evento_id', eventoId);
    formData.append('acao', acao);

    // Verifica se a ação é "confirmar" para manipular a confirmação do evento
    if (acao === 'confirmar') {
        // Envia a requisição para confirmar a ocorrência do evento
        fetch('/acao_evento', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('Evento finalizado e prêmios distribuídos.');
                location.reload(); // Recarrega a página após a ação
            } else {
                alert('Ocorreu um erro ao finalizar o evento.');
            }
        })
        .catch(error => {
            console.error('Erro ao enviar a requisição:', error);
            alert('Erro ao enviar a requisição.');
        });
    } else {
        // Envia a requisição para aprovar ou reprovar o evento
        fetch('/acao_evento', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                if (acao === 'aprovar') {
                    alert('Evento aprovado com sucesso.');
                } else {
                    alert('Evento reprovado com sucesso.');
                }
                location.reload(); // Recarrega a página após a ação
            } else {
                alert('Ocorreu um erro ao processar a ação do evento.');
            }
        })
        .catch(error => {
            console.error('Erro ao enviar a requisição:', error);
            alert('Erro ao enviar a requisição.');
        });
    }
}

// Função para abrir o modal de reprovação
function abrirModalReprovar(eventoId) {
    document.getElementById('modalEventoId').value = eventoId; // Define o ID do evento no modal
    document.getElementById('modalReprovar').style.display = 'block'; // Mostra o modal
}

// Fecha o modal ao clicar no botão de fechar
document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('modalReprovar').style.display = 'none';
});

// Fecha o modal ao clicar fora dele
window.onclick = function(event) {
    if (event.target == document.getElementById('modalReprovar')) {
        document.getElementById('modalReprovar').style.display = 'none';
    }
};
