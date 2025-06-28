
import requests
from django.core.management.base import BaseCommand
from loja.models import Produto
from django.core.files.base import ContentFile
from django.utils.text import slugify
import os
from urllib.parse import urlparse
from urllib.request import urlopen

class Command(BaseCommand):
    help = 'Importa produtos da Fake Store API e salva no banco de dados'

    def handle(self, *args, **kwargs):
        url = 'https://fakestoreapi.com/products'
        response = requests.get(url)
        produtos = response.json()

        mapeamento_categorias = {
            'electronics': 'eletronicos',
            'jewelery': 'acessorios',
            "men's clothing": 'roupas',
            "women's clothing": 'roupas'
        }

        total_importados = 0
        for item in produtos:
            nome = item['title']
            preco = float(item['price'])
            descricao = item['description']
            imagem_url = item['image']
            categoria_api = item['category']
            categoria = mapeamento_categorias.get(categoria_api, 'outros')

            # Evitar duplicatas
            if Produto.objects.filter(nome=nome).exists():
                self.stdout.write(self.style.WARNING(f"Produto já existe: {nome}"))
                continue

            produto = Produto(
                nome=nome,
                preço=preco,
                descricao=descricao,
                descricao_longa=descricao,
                categoria=categoria,
                estoque=10,
                digital=False
            )

            # Baixar imagem
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(imagem_url, headers=headers)
                r.raise_for_status()  # lança erro se não for 200
                imagem_nome = os.path.basename(urlparse(imagem_url).path)
                produto.imagem.save(imagem_nome, ContentFile(r.content), save=False)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Erro ao baixar imagem para {nome}: {e}"))


            try:
                produto.save()
                total_importados += 1
                self.stdout.write(self.style.SUCCESS(f"Produto importado: {nome}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao salvar produto '{nome}': {e}"))