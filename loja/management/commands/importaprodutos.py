import requests
from django.core.management.base import BaseCommand
from loja.models import Produto
from django.core.files.base import ContentFile
from django.utils.text import slugify
from decimal import Decimal
import os
from urllib.parse import urlparse


class Command(BaseCommand):
    help = 'Importa produtos da API DummyJSON para o banco de dados'

    def handle(self, *args, **options):
        url = 'https://dummyjson.com/products?limit=50'
        response = requests.get(url)
        data = response.json()
        produtos = data.get('products', [])

        contador = 0

        for p in produtos:
            nome = p['title']
            preco = Decimal(p['price'])
            descricao = p['description']
            categoria = p['category']
            imagem_url = p['thumbnail']

            # Mapear categoria externa para suas categorias
            categoria_mapeada = self.mapear_categoria(categoria)

            # Evitar duplicatas
            if Produto.objects.filter(nome=nome).exists():
                continue

            produto = Produto(
                nome=nome,
                preço=preco,
                descricao=descricao,
                categoria=categoria_mapeada,
                estoque=p.get('stock', 10),
                digital=False,
            )

            # Imagem principal
            if imagem_url:
                try:
                    img_data = requests.get(imagem_url).content
                    nome_arquivo = os.path.basename(urlparse(imagem_url).path)
                    produto.imagem.save(nome_arquivo, ContentFile(img_data), save=False)
                except:
                    pass

            produto.save()
            contador += 1

        self.stdout.write(self.style.SUCCESS(f'{contador} produtos importados com sucesso.'))

    def mapear_categoria(self, cat):
        """
        Mapeia a categoria externa para as do seu sistema
        """
        mapa = {
            'smartphones': 'eletronicos',
            'laptops': 'eletronicos',
            'fragrances': 'outros',
            'skincare': 'outros',
            'groceries': 'outros',
            'home-decoration': 'outros',
            'furniture': 'outros',
            'tops': 'roupas',
            'womens-dresses': 'roupas',
            'womens-shoes': 'roupas',
            'mens-shirts': 'roupas',
            'mens-shoes': 'roupas',
            'mens-watches': 'acessorios',
            'womens-watches': 'acessorios',
            'womens-bags': 'acessorios',
            'womens-jewellery': 'acessorios',
            'sunglasses': 'acessorios',
            'automotive': 'outros',
            'motorcycle': 'outros',
            'lighting': 'outros',
        }
        return mapa.get(cat, 'outros')
