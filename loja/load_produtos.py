import os
import json
from loja.models import Produto

def carregar_produtos():
    # Caminho até a raiz do projeto (onde está o manage.py e o JSON)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'produtos_moda.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)

        for item in dados:
            Produto.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'nome': item['nome'],
                    'descricao': item['descricao'],
                    'preço': item['preço'],
                    'preco_desconto': item.get('preco_desconto'),
                    'categoria': item['categoria'],
                    'imagem': item['imagem'],
                }
            )
