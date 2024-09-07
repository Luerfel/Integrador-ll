function abrirPopup() {
    document.getElementById('popup').style.display = 'block';
    document.getElementById('popup-overlay').style.display = 'block';
}

function fecharPopup() {
    document.getElementById('popup').style.display = 'none';
    document.getElementById('popup-overlay').style.display = 'none';
}

// Adiciona event listener apenas para o botão "Adicionar créditos"
document.addEventListener('DOMContentLoaded', function() {
    const botaoAdicionarCreditos = document.querySelector('.btn-adicionar-creditos');
    if (botaoAdicionarCreditos) {
        botaoAdicionarCreditos.addEventListener('click', abrirPopup);
    }

    document.getElementById('popup-overlay').addEventListener('click', fecharPopup);
    document.getElementById('popup').querySelector('.btn-close').addEventListener('click', fecharPopup);
});
