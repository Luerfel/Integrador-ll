document.getElementById('apostar-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Previne o comportamento padrão
    document.getElementById('apostar-form').submit(); // Submete o formulário manualmente
});
