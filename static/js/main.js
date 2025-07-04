var user = '{{ request.user }}';

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getToken('csrftoken');

function getCookie(name) {
    const cookieArr = document.cookie.split(";");
    for (const cookiePair of cookieArr) {
        const [key, value] = cookiePair.trim().split("=");
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}

let cart = JSON.parse(getCookie('cart') || '{}');
if (!cart || Object.keys(cart).length === 0) {
    cart = {};
    document.cookie = 'cart=' + JSON.stringify(cart) + ';path=/;SameSite=Lax';
}
console.log('Cart:', cart);

document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('toggle-dark');

  const savedTheme = localStorage.getItem('tema');
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark-mode');
  } else {
    document.documentElement.classList.remove('dark-mode');
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark-mode');
      const tema = isDark ? 'dark' : 'light';
      localStorage.setItem('tema', tema);
      document.cookie = `tema=${tema};path=/;SameSite=Lax`;
    });
  } else {
    console.warn('[DarkMode] Botão não encontrado.');
  }

  // Comprar Agora - adiciona item e redireciona para checkout
  document.querySelectorAll('.buy-now').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const productId = this.dataset.product;
      const action = this.dataset.action;

      fetch('/atualizacaoitem/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ productId, action })
      })
        .then(response => response.json())
        .then(data => {
          console.log('Item adicionado para compra imediata:', data);
          window.location.href = '/checkout/';
        });
    });
  });
});

// Atualiza o número de itens no carrinho ao voltar para a página
window.addEventListener("pageshow", function (event) {
  if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
    fetch('/carrinho/quantidade/')
      .then(response => response.json())
      .then(data => {
        const cartCount = document.getElementById('cart-total');
        if (cartCount) {
          cartCount.textContent = data.total_itens;
        }
      });
  }
});


// Detecta se a página foi carregada via cache (ex: botão voltar do navegador)
window.addEventListener('pageshow', function (event) {
  if (event.persisted || (window.performance && performance.getEntriesByType("navigation")[0].type === "back_forward")) {
    location.reload(); // Recarrega para garantir que o carrinho esteja atualizado
  }
});
