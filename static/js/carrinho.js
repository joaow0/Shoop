const buttons = document.querySelectorAll('.update-cart');

buttons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation(); // 👈 garante que não propague para o link pai

        const productId = button.dataset.product;
        const action = button.dataset.action;
        updateCarrinho(productId, action);
    });
});


function updateCarrinho(productId, action) {
    const url = '/atualizacaoitem/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then(res => res.json())
    .then(data => {
        console.log('Resposta do servidor:', data);

        // Atualiza o ícone do carrinho
        const cartTotal = document.getElementById('cart-total');
        if (cartTotal && data.total_itens !== undefined) {
            cartTotal.innerText = data.total_itens;
        }

        // Atualiza a quantidade e total do produto individual
        if (data.produto_id !== undefined) {
            const quantidadeEl = document.querySelector(`[data-quantidade-produto="${data.produto_id}"]`);
            const totalEl = document.querySelector(`[data-total-produto="${data.produto_id}"]`);

            if (quantidadeEl) quantidadeEl.innerText = data.quantidade;
            if (totalEl) totalEl.innerText = `R$ ${parseFloat(data.total_produto).toFixed(2).replace('.', ',')}`;
        }

        // Atualiza o total do pedido no topo
        const totalPedidoEl = document.getElementById('total-pedido');
        const totalItensEl = document.getElementById('total-itens');

        if (totalPedidoEl && data.total_pedido !== undefined) {
            totalPedidoEl.innerText = `R$ ${parseFloat(data.total_pedido).toFixed(2).replace('.', ',')}`;
        }

        if (totalItensEl && data.total_itens !== undefined) {
            totalItensEl.innerText = data.total_itens;
        }
    });
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}
