from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import cookiecarrinho, carrinhodata, pedidoguest
from django.contrib import messages
from django.db.models import Avg  # importante pra aggregate funcionar sem erro
from random import sample

def loja(request):
    data = carrinhodata(request)
    produtos = Produto.objects.all()

    # Filtros
    categoria = request.GET.get('categoria')
    ordenacao = request.GET.get('ordenar')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if categoria and categoria != 'todos':
        produtos = produtos.filter(categoria=categoria)

    if preco_min:
        produtos = produtos.filter(preço__gte=preco_min)

    if preco_max:
        produtos = produtos.filter(preço__lte=preco_max)

    if ordenacao == 'menor_preco':
        produtos = produtos.order_by('preço')
    elif ordenacao == 'maior_preco':
        produtos = produtos.order_by('-preço')
    elif ordenacao == 'a_z':
        produtos = produtos.order_by('nome')
    elif ordenacao == 'z_a':
        produtos = produtos.order_by('-nome')

    contexto = {
        'produtos': produtos,
        'carrinhoitens': data['carrinhoitens'],
        'categoria_selecionada': categoria,
    }
    return render(request, 'loja/loja.html', contexto)


def carrinho(request):
    data = carrinhodata(request)
    contexto = {
        'itens': data['itens'],
        'pedido': data['pedido'],
        'carrinhoitens': data['carrinhoitens']
    }
    return render(request, 'loja/carrinho.html', contexto)



def checkout(request):
    data = carrinhodata(request)
    contexto = {
        'itens': data['itens'],
        'pedido': data['pedido'],
        'carrinhoitens': data['carrinhoitens']
    }
    return render(request, 'loja/checkout.html', contexto)



@csrf_exempt
def atualizacaoitem(request):
    data = json.loads(request.body)
    produto_id = data['productId']
    action = data['action']

    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado.'}, status=404)

    if request.user.is_authenticated:
        cliente, _ = Customer.objects.get_or_create(
            usuario=request.user,
            defaults={'nome': request.user.username, 'email': request.user.email}
        )

        pedido, _ = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        pedido_item, _ = PedidoItem.objects.get_or_create(pedido=pedido, produto=produto)

        if action == 'add':
            pedido_item.quantidade += 1
        elif action == 'remove':
            pedido_item.quantidade -= 1

        pedido_item.save()

        if pedido_item.quantidade <= 0:
            pedido_item.delete()

        total_itens = pedido.get_cart_items  # <-- seu método @property

        return JsonResponse({'mensagem': 'Item atualizado!', 'total_itens': total_itens})

    else:
        carrinho = json.loads(request.COOKIES.get('cart', '{}'))

        if action == 'add':
            if str(produto_id) in carrinho:
                carrinho[str(produto_id)]['quantidade'] += 1
            else:
                carrinho[str(produto_id)] = {'quantidade': 1}
        elif action == 'remove':
            if str(produto_id) in carrinho:
                carrinho[str(produto_id)]['quantidade'] -= 1
                if carrinho[str(produto_id)]['quantidade'] <= 0:
                    del carrinho[str(produto_id)]

        # Calcula total de itens no carrinho (para usuários anônimos)
        total_itens = sum(item['quantidade'] for item in carrinho.values())

        response = JsonResponse({
            'mensagem': 'Item atualizado no carrinho!',
            'total_itens': total_itens
        })
        response.set_cookie('cart', json.dumps(carrinho))
        return response



@csrf_exempt
def pedidoProcesso(request):
    if request.user.is_authenticated:
        cliente, _ = Customer.objects.get_or_create(usuario=request.user)
        pedido = Pedido.objects.filter(cliente=cliente, completo=False).first()
        if pedido is None:
            pedido = Pedido.objects.create(cliente=cliente, completo=False)
    else:
        cliente, pedido = pedidoguest(request, data)




def sobre(request):
    return render(request, 'loja/sobre.html')







def produtoDetalhes(request, pk):
    produto = Produto.objects.get(id=pk)
    avaliacoes = Avaliacao.objects.filter(produto=produto)

    media = avaliacoes.aggregate(Avg('nota'))['nota__avg'] or 0
    media = round(media, 1)

    data = carrinhodata(request)

    contexto = {
        'produto': produto,
        'avaliacoes': avaliacoes,
        'media': media,
        'carrinhoitens': data['carrinhoitens']
    }
    return render(request, 'loja/produto.html', contexto)





def produtoDetalhes(request, pk):
    produto = get_object_or_404(Produto, id=pk)
    avaliacoes = Avaliacao.objects.filter(produto=produto)
    media = avaliacoes.aggregate(Avg('nota'))['nota__avg'] or 0
    media = round(media, 1)

    data = carrinhodata(request)

    if request.method == 'POST':
        if request.user.is_authenticated:
            cliente = Customer.objects.get(usuario=request.user)
            nota = int(request.POST.get('nota'))
            comentario = request.POST.get('comentario')

            avaliacao, created = Avaliacao.objects.get_or_create(
                cliente=cliente,
                produto=produto,
                defaults={'nota': nota, 'comentario': comentario}
            )

            if not created:
                messages.error(request, 'Você já avaliou este produto.')
            else:
                messages.success(request, 'Avaliação enviada com sucesso!')

            return redirect('produto', pk=produto.id)
        else:
            messages.error(request, 'Você precisa estar logado para avaliar.')
            return redirect('login')

    contexto = {
        'produto': produto,
        'avaliacoes': avaliacoes,
        'media': media,
        'carrinhoitens': data['carrinhoitens']
    }
    return render(request, 'loja/produto.html', contexto)




def produtoDetalhes(request, pk):
    produto = get_object_or_404(Produto, id=pk)
    avaliacoes = Avaliacao.objects.filter(produto=produto)

    media = avaliacoes.aggregate(Avg('nota'))['nota__avg'] or 0
    media = round(media, 1)

    data = carrinhodata(request)

    # Produtos recomendados (excluindo o atual)
    outros_produtos = Produto.objects.exclude(id=produto.id)
    recomendados = sample(list(outros_produtos), min(4, outros_produtos.count()))

    contexto = {
        'produto': produto,
        'avaliacoes': avaliacoes,
        'media': media,
        'carrinhoitens': data['carrinhoitens'],
        'recomendados': recomendados,
    }
    return render(request, 'loja/produto.html', contexto)






def pesquisa(request):
    data = carrinhodata(request)
    query = request.GET.get('q', '')
    produtos = Produto.objects.filter(nome__icontains=query) if query else Produto.objects.none()

    # Filtros
    categoria = request.GET.get('categoria')
    ordenar = request.GET.get('ordenar')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if categoria and categoria != 'todos':
        produtos = produtos.filter(categoria=categoria)

    if preco_min:
        produtos = produtos.filter(preço__gte=preco_min)

    if preco_max:
        produtos = produtos.filter(preço__lte=preco_max)

    if ordenar == 'menor_preco':
        produtos = produtos.order_by('preço')
    elif ordenar == 'maior_preco':
        produtos = produtos.order_by('-preço')
    elif ordenar == 'a_z':
        produtos = produtos.order_by('nome')
    elif ordenar == 'z_a':
        produtos = produtos.order_by('-nome')

    contexto = {
        'produtos': produtos,
        'carrinhoitens': data['carrinhoitens'],
        'query': query,
        'categoria_selecionada': categoria,
        'preco_min': preco_min,
        'preco_max': preco_max,
        'ordenar': ordenar,
    }
    return render(request, 'loja/pesquisa.html', contexto)
