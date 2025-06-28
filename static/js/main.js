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

  // Força o modo escuro caso localStorage diga isso (garantia)
  const savedTheme = localStorage.getItem('tema');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
  }

  // Clique no botão para alternar
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-mode');
      const tema = isDark ? 'dark' : 'light';
      localStorage.setItem('tema', tema);

      // Salvar também em cookie (para uso no backend)
      document.cookie = `tema=${tema};path=/;SameSite=Lax`;
    });
  }
});
