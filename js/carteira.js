// Seleciona os botões e modais
const btnAdicionarCreditos = document.getElementById('btn-adicionar-creditos');
const btnSacar = document.getElementById('btn-sacar');
const modalAdicionar = document.getElementById('modal-adicionar');
const modalSacar = document.getElementById('modal-sacar');
const closeAdicionar = document.getElementById('close-adicionar');
const closeSacar = document.getElementById('close-sacar');

function formatarSaldo(saldo) {
    // Garante que o saldo seja uma string
    saldo = saldo.toString();

    // Se o saldo for menor que 1, ajustamos a parte inteira com zeros
    let inteiro = saldo.split('.')[0]; // Parte inteira
    let decimal = saldo.split('.')[1] || '00'; // Parte decimal, se não existir, coloca '00'

    // Se a parte inteira for menor que 6 dígitos, preenche com zeros à esquerda
    inteiro = inteiro.padStart(6, '0');

    // Adiciona pontos a cada 3 dígitos na parte inteira
    inteiro = inteiro; //

    // Garantir que a parte decimal tenha exatamente 2 dígitos
    decimal = decimal.padEnd(2, '0');

    // Formatar a parte inteira e decimal com zeros roxos
    return 'R$ ' + formatarComZeros(inteiro, decimal);
}

// Função para aplicar a formatação correta com zeros em roxo
function formatarComZeros(parteInteira, parteDecimal) {
    // Formatação da parte inteira e decimal, aplicando a cor roxa nos zeros
    let saldoFormatado;
    if (parteInteira > 0){
    saldoFormatado = parteInteira.replace(/^0+(?=\d)/g, (match) => {

        return match.replace(/0/g, '<span class="zeros">0</span>');
    
    });}else{
        saldoFormatado = parteInteira.replace(/0/g, (match) => {

            return match.replace(/0/g, '<span class="zeros">0</span>');
        
        });  
    }
    
    if (parteInteira > 99999 ){
        saldoFormatado = saldoFormatado.replace(/\B(?=(\d{3})+(?!\d))/, ',');
    }else if (/(<span class="zeros">0<\/span>){3}/.test(saldoFormatado)) {
        saldoFormatado = saldoFormatado.replace(/(<span class="zeros">0<\/span>){3}/, '$&,');
    } else if (/(<span class="zeros">0<\/span>){2}(\d)/.test(saldoFormatado)) {
        saldoFormatado = saldoFormatado.replace(/(<span class="zeros">0<\/span>){2}(\d)/, '$&,');
    } else if (/(<span class="zeros">0<\/span>)(\d{2})/.test(saldoFormatado)) {
        saldoFormatado = saldoFormatado.replace(/(<span class="zeros">0<\/span>)(\d{2})/, '$&,');
    }
    console.log(saldoFormatado);
    if (/0<\/span>,(\d)/.test(saldoFormatado)) {
        saldoFormatado = saldoFormatado.replace(/0<\/span>,(\d)/, '0</span><span class="zeros">,</span>$1');
    }else if (/0<\/span>,<span/.test(saldoFormatado)) {
        saldoFormatado = saldoFormatado.replace(/(0<\/span>),/, '$1<span class="zeros">,</span>');
    }
    //saldoFormatado = saldoFormatado.replace(/0<\/span>,(\d)/, '0</span><span class="zeros">,</span>$1');
    
   
    saldoFormatado += '.' + parteDecimal;

    return saldoFormatado;
}

document.addEventListener('DOMContentLoaded', function () {
    const saldoElement = document.querySelector('.saldo_total');
    const saldoRaw = saldoElement.textContent.trim(); // Pega o texto dentro do elemento
    const saldo = parseFloat(saldoRaw); // Converte para número
    if (!isNaN(saldo)) {
        saldoElement.innerHTML  = formatarSaldo(saldo); // Formata e insere o saldo
    } else {
        saldoElement.innerHTML  = 'Saldo inválido'; // Caso o saldo seja inválido
    }
});
// Abre o modal de adicionar créditos
btnAdicionarCreditos.addEventListener('click', function() {
    modalAdicionar.style.display = 'block';
});

// Fecha o modal de adicionar créditos
closeAdicionar.addEventListener('click', function() {
    modalAdicionar.style.display = 'none';
});

// Abre o modal de saque
btnSacar.addEventListener('click', function() {
    modalSacar.style.display = 'block';
});

// Fecha o modal de saque
closeSacar.addEventListener('click', function() {
    modalSacar.style.display = 'none';
});

// Fecha o modal ao clicar fora dele
window.addEventListener('click', function(event) {
    if (event.target == modalAdicionar) {
        modalAdicionar.style.display = 'none';
    }
    if (event.target == modalSacar) {
        modalSacar.style.display = 'none';
    }
});

// Mostrar campos com base no método de saque selecionado
const metodoBanco = document.getElementById('metodo_banco');
const metodoPix = document.getElementById('metodo_pix');
const camposBanco = document.getElementById('campos-banco');
const camposPix = document.getElementById('campos-pix');

metodoBanco.addEventListener('change', function() {
    if (this.checked) {
        camposBanco.style.display = 'block';
        camposPix.style.display = 'none';
    }
});

metodoPix.addEventListener('change', function() {
    if (this.checked) {
        camposBanco.style.display = 'none';
        camposPix.style.display = 'block';
    }
});
// Botões e modais para o histórico de transações
const btnVerTransacoes = document.getElementById('btn-ver-transacoes');
const modalTransacoes = document.getElementById('modal-transacoes');
const closeTransacoes = document.getElementById('close-transacoes');

btnVerTransacoes.addEventListener('click', function() {
    modalTransacoes.style.display = 'block';
});

closeTransacoes.addEventListener('click', function() {
    modalTransacoes.style.display = 'none';
});

// Botões e modais para o histórico de apostas
const btnVerApostas = document.getElementById('btn-ver-apostas');
const modalApostas = document.getElementById('modal-apostas');
const closeApostas = document.getElementById('close-apostas');

btnVerApostas.addEventListener('click', function() {
    modalApostas.style.display = 'block';
});

closeApostas.addEventListener('click', function() {
    modalApostas.style.display = 'none';
});

// Fechar modais ao clicar fora deles
window.addEventListener('click', function(event) {
    if (event.target == modalTransacoes) {
        modalTransacoes.style.display = 'none';
    }
    if (event.target == modalApostas) {
        modalApostas.style.display = 'none';
    }
});
// Seleciona os elementos
const valorSaqueInput = document.getElementById('valor_saque');
const taxaAplicadaSpan = document.getElementById('taxa_aplicada');
const valorLiquidoSpan = document.getElementById('valor_liquido');

// Função para calcular a taxa e o valor líquido
function calcularTaxaEValorLiquido() {
    let valorSaque = parseFloat(valorSaqueInput.value);

    if (isNaN(valorSaque) || valorSaque <= 0) {
        taxaAplicadaSpan.textContent = '0.00';
        valorLiquidoSpan.textContent = '0.00';
        return;
    }

    let taxa = 0;

    if (valorSaque <= 100) {
        taxa = 0.04 * valorSaque;
    } else if (valorSaque <= 1000) {
        taxa = 0.03 * valorSaque;
    } else if (valorSaque <= 5000) {
        taxa = 0.02 * valorSaque;
    } else if (valorSaque <= 100000) {
        taxa = 0.01 * valorSaque;
    } else {
        taxa = 0.00; // Isento
    }

    let valorLiquido = valorSaque - taxa;

    // Atualiza os valores nos elementos HTML
    taxaAplicadaSpan.textContent = taxa.toFixed(2);
    valorLiquidoSpan.textContent = valorLiquido.toFixed(2);
}

// Adiciona um listener ao campo de valor de saque
valorSaqueInput.addEventListener('input', calcularTaxaEValorLiquido);
