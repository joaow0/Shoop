
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('toggle-dark');
  const body = document.body;

  // Aplicar tema salvo
  const tema = localStorage.getItem('tema');
  if (tema === 'dark') {
    body.classList.add('dark-mode');
  }

  // Trocar tema
  if (toggle) {
    toggle.addEventListener('click', function () {
      body.classList.toggle('dark-mode');
      localStorage.setItem('tema', body.classList.contains('dark-mode') ? 'dark' : 'light');
    });
  }

  // Simular fetch carrinho (comentado por segurança)
  // const updateBtns = document.querySelectorAll('.update-cart');
  // updateBtns.forEach(btn => {
  //   btn.addEventListener('click', function () {
  //     const productId = this.dataset.product;
  //     const action = this.dataset.action;
  //     fetch('/atualizar_item/', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //         'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
  //       },
  //       body: JSON.stringify({ productId, action })
  //     }).then(res => res.json()).then(data => {
  //       location.reload();
  //     });
  //   });
  // });
});
