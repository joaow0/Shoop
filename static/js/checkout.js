const formulario = document.getElementById('formulario');
const pagamentoInfo = document.getElementById('payment-info');
const botaoContinuar = document.getElementById('form-button');

formulario.addEventListener('submit', function (e) {
    e.preventDefault();
    pagamentoInfo.classList.remove('hidden');
    botaoContinuar.classList.add('hidden');
});

const metodoPagamento = document.getElementById('metodo-pagamento');
const metodos = document.querySelectorAll('.metodo');

metodoPagamento.addEventListener('change', function () {
    metodos.forEach(div => div.classList.add('hidden'));
    const metodoSelecionado = this.value;

    if (metodoSelecionado === 'pix') {
        document.getElementById('pagamento-pix').classList.remove('hidden');
    } else if (metodoSelecionado === 'cartao') {
        document.getElementById('pagamento-cartao').classList.remove('hidden');
    } else if (metodoSelecionado === 'boleto') {
        document.getElementById('pagamento-boleto').classList.remove('hidden');
    }
});

// PayPal
paypal.Buttons({
    createOrder: function(data, actions) {
        return fetch('/demo/checkout/api/paypal/order/create/', {
            method: 'post'
        }).then(res => res.json()).then(orderData => orderData.id);
    },
    onApprove: function(data, actions) {
        return fetch('/demo/checkout/api/paypal/order/' + data.orderID + '/capture/', {
            method: 'post'
        }).then(res => res.json()).then(orderData => {
            const errorDetail = Array.isArray(orderData.details) && orderData.details[0];
            if (errorDetail && errorDetail.issue === 'INSTRUMENT_DECLINED') {
                return actions.restart();
            }
            if (errorDetail) {
                let msg = 'Desculpe, sua transação não pôde ser processada.';
                if (errorDetail.description) msg += '\n\n' + errorDetail.description;
                if (orderData.debug_id) msg += ' (' + orderData.debug_id + ')';
                return alert(msg);
            }
            const transaction = orderData.purchase_units[0].payments.captures[0];
            alert('Transação ' + transaction.status + ': ' + transaction.id);
            window.location.href = '/';
        });
    }
}).render('#paypal-button-container');

