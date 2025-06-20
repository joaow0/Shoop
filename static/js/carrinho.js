// Primeiro: pegar o CSRF token

// Segundo: ouvir cliques nos botões de update-cart
var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            console.log('Não está logado');
        } else {
            console.log('O usuário está logado, enviando dados');
            atualizaçãousuariopedido(productId, action);
        }
    })
}


function adicionaritemcarrinho(productId, action){
    console.log('Usuário anônimo - atualizando cookie');

    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = { 'quantidade': 1 };
        } else {
            cart[productId]['quantidade'] += 1;
        }
    }

    if (action === 'remove') {
        cart[productId]['quantidade'] -= 1;

        if (cart[productId]['quantidade'] <= 0) {
            console.log('Remover item');
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);

    // CORREÇÃO CRÍTICA:
    document.cookie = "cart=" + JSON.stringify(cart) + ";path=/;SameSite=Lax";

    location.reload();
}



// Terceiro: enviar requisição via fetch
function atualizaçãousuariopedido(productId, action) {
    console.log('O usuário está conectado, enviando dados');

    var url = '/atualizaçãoitem/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload() // Atualiza a página depois de adicionar/remover item
        
    });
}


var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Produto ID:', productId, 'Ação:', action)

        adicionaritemcarrinho(productId, action)
    })
}
