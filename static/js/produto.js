// static/js/produto.js - ATUALIZADO

function trocarImagem(src, thumb) {
    const principal = document.getElementById('imagem-principal');
    const zoomPreview = document.getElementById('zoom-preview');

    principal.src = src;
    zoomPreview.style.backgroundImage = `url('${src}')`;

    document.querySelectorAll('.galeria-thumbs img').forEach(img => {
        img.classList.remove('active');
    });

    if (thumb) {
        thumb.classList.add('active');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.zoom-container');
    const img = document.getElementById('imagem-principal');
    const preview = document.getElementById('zoom-preview');

    if (!img || !preview || !container) return;

    const zoom = 2;

    preview.style.backgroundImage = `url('${img.src}')`;
    preview.style.backgroundRepeat = 'no-repeat';
    preview.style.backgroundSize = `${img.width * zoom}px ${img.height * zoom}px`;

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const bgX = (x / container.offsetWidth) * 100;
        const bgY = (y / container.offsetHeight) * 100;

        preview.style.display = 'block';
        preview.style.backgroundPosition = `${bgX}% ${bgY}%`;
    });

    container.addEventListener('mouseenter', () => {
        preview.style.display = 'block';
    });

    container.addEventListener('mouseleave', () => {
        preview.style.display = 'none';
    });

    img.addEventListener('load', () => {
        preview.style.backgroundImage = `url('${img.src}')`;
        preview.style.backgroundSize = `${img.width * zoom}px ${img.height * zoom}px`;
    });
});

function scrollContainer(direction) {
    const container = document.getElementById('scroll-container');
    const scrollAmount = 300;
    if (direction === 'left') {
        container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
        container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
}