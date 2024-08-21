function handleEventAction(eventId, action) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/acao_evento", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Remove o evento da lista após a ação ser bem-sucedida
                const eventRow = document.getElementById(`event-${eventId}`);
                if (eventRow) {
                    eventRow.remove();
                }
            } else {
                alert('Ocorreu um erro ao processar a ação. Tente novamente.');
            }
        }
    };

    xhr.send(`evento_id=${eventId}&acao=${action}`);
}
