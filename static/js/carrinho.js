// Formatador de moeda BR
function formatarMoedaBR(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

const buttons = document.querySelectorAll('.update-cart');

buttons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        const productId = button.dataset.product;
        const action = button.dataset.action;
        updateCarrinho(productId, action);
    });
});

function updateCarrinho(productId, action) {
    if (!user || user === 'AnonymousUser' || user.includes('Anonymous')) {
        updateCartCookie(productId, action);
        return;
    }

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

        const cartTotal = document.getElementById('cart-total');
        if (cartTotal && data.total_itens !== undefined) {
            cartTotal.innerText = data.total_itens;
        }

        if (window.location.pathname === '/carrinho/' || window.location.pathname.startsWith('/carrinho')) {
            atualizarCarrinhoDOM(data);
        }
    });
}

// Atualiza a interface para usuários anônimos (via cookies)
function updateCartCookie(productId, action) {
    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ';path=/;SameSite=Lax';

    const total = Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
    const cartTotal = document.getElementById('cart-total');
    if (cartTotal) {
        cartTotal.innerText = total;
    }

    if (window.location.pathname === '/carrinho/' || window.location.pathname.startsWith('/carrinho')) {
        const linhaProdutoEl = document.querySelector(`[data-prod-linha="${productId}"]`);
        const quantidadeEl = document.querySelector(`[data-quantidade-produto="${productId}"]`);
        const totalEl = document.querySelector(`[data-total-produto="${productId}"]`);

        if (cart[productId]) {
            const produtoPreco = parseFloat(totalEl.dataset.preco);
            const novaQtd = cart[productId].quantity;
            const novoTotal = produtoPreco * novaQtd;

            if (quantidadeEl) quantidadeEl.innerText = novaQtd;
            if (totalEl) totalEl.innerText = formatarMoedaBR(novoTotal);
        } else {
            if (linhaProdutoEl) linhaProdutoEl.remove();
        }

        let novoTotalPedido = 0;
        let novoTotalItens = 0;

        document.querySelectorAll('[data-total-produto]').forEach(el => {
            const texto = el.innerText.replace(/[^\d,]/g, '').replace(',', '.');
            novoTotalPedido += parseFloat(texto);
        });

        document.querySelectorAll('[data-quantidade-produto]').forEach(el => {
            novoTotalItens += parseInt(el.innerText);
        });

        const totalPedidoEl = document.querySelector('.card-body h5:nth-of-type(2) strong');
        const itensCarrinhoCardEl = document.querySelector('.card-body h5:nth-of-type(1) strong');

        if (totalPedidoEl) totalPedidoEl.innerText = formatarMoedaBR(novoTotalPedido);
        if (itensCarrinhoCardEl) itensCarrinhoCardEl.innerText = novoTotalItens;

        if (novoTotalItens === 0) {
            const cartContainer = document.querySelector('.container.my-4');
            const cardItems = document.querySelector('.card.shadow-sm:nth-of-type(2)');
            const finalizarCompraCard = document.querySelector('.card.shadow-sm.mb-4');

            if (cardItems) cardItems.remove();
            if (finalizarCompraCard) finalizarCompraCard.remove();

            const emptyCartMessage = document.createElement('div');
            emptyCartMessage.className = 'alert alert-info text-center';
            emptyCartMessage.innerText = 'Seu carrinho está vazio!';
            cartContainer.appendChild(emptyCartMessage);
        }
    }
}

// Atualiza a DOM para usuários logados
function atualizarCarrinhoDOM(data) {
    const quantidadeEl = document.querySelector(`[data-quantidade-produto="${data.produto_id}"]`);
    const totalEl = document.querySelector(`[data-total-produto="${data.produto_id}"]`);
    const linhaProdutoEl = document.querySelector(`[data-prod-linha="${data.produto_id}"]`);

    if (data.quantidade > 0) {
        if (quantidadeEl) quantidadeEl.innerText = data.quantidade;
        if (totalEl) totalEl.innerText = formatarMoedaBR(data.total_produto);
    } else {
        if (linhaProdutoEl) linhaProdutoEl.remove();
    }

    const totalPedidoEl = document.querySelector('.card-body h5:nth-of-type(2) strong');
    const itensCarrinhoCardEl = document.querySelector('.card-body h5:nth-of-type(1) strong');

    if (totalPedidoEl && data.total_pedido !== undefined) {
        totalPedidoEl.innerText = formatarMoedaBR(data.total_pedido);
    }

    if (itensCarrinhoCardEl && data.total_itens !== undefined) {
        itensCarrinhoCardEl.innerText = data.total_itens;
    }

    if (data.total_itens === 0) {
        const cartContainer = document.querySelector('.container.my-4');
        const cardItems = document.querySelector('.card.shadow-sm:nth-of-type(2)');
        const finalizarCompraCard = document.querySelector('.card.shadow-sm.mb-4');

        if (cardItems) cardItems.remove();
        if (finalizarCompraCard) finalizarCompraCard.remove();

        const emptyCartMessage = document.createElement('div');
        emptyCartMessage.className = 'alert alert-info text-center';
        emptyCartMessage.innerText = 'Seu carrinho está vazio!';
        cartContainer.appendChild(emptyCartMessage);
    }
}

// Coleta o cookie CSRF
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
