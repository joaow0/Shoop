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
        console.log('Item atualizado:', data);

        const cartTotal = document.getElementById('cart-total');
        if (cartTotal && data.total_itens !== undefined) {
            cartTotal.innerText = data.total_itens;
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
