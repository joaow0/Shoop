# loja/context_processors.py

from .utils import carrinhodata

def categorias_disponiveis(request):
    return {
        'categorias': [
            {'slug': 'eletronicos', 'nome': 'Eletrônicos'},
            {'slug': 'roupas', 'nome': 'Roupas'},
            {'slug': 'livros', 'nome': 'Livros'},
            {'slug': 'acessorios', 'nome': 'Acessórios'},
            {'slug': 'outros', 'nome': 'Outros'},
        ]
    }

def carrinho_contexto(request):
    data = carrinhodata(request)
    return {
        'carrinhoitens': data['carrinhoitens']
    }
