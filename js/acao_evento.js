// Seleciona todos os botões com a classe 'btn-acao' e adiciona um listener para o evento de clique
document.querySelectorAll('.btn-acao').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        // Obtém os atributos 'data-evento-id' e 'data-acao' para identificar o evento e a ação
        const eventoId = this.getAttribute('data-evento-id');
        const acao = this.getAttribute('data-acao');
        const motivoRejeicao = document.querySelector(`#motivo_${eventoId}`)?.value || '';

        // Faz a requisição para a rota '/acao_evento' enviando o evento_id e a ação selecionada
        fetch('/acao_evento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                evento_id: eventoId,
                acao: acao,
                motivo_rejeicao: motivoRejeicao
            })
        })
        .then(response => response.json())  // Converte a resposta para JSON
        .then(data => {
            // Exibe uma mensagem de sucesso ou erro com base na resposta da rota
            if (data.success) {
                alert(data.message);  // Janela com mensagem de sucesso
            } else {
                alert(data.message);  // Janela com mensagem de erro
            }
        })
        .catch(error => {
            alert("Erro na requisição.");  // Mensagem de erro de rede
            console.error('Erro:', error);
        });
    });
});
