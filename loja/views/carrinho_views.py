from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from loja.models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from loja.utils import carrinhodata

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

        if pedido_item.quantidade <= 0:
            pedido_item.delete()
        else:
            pedido_item.save()

        # Atualiza os valores
        total_itens = pedido.get_cart_items
        total_pedido = pedido.get_cart_total
        total_produto = pedido_item.get_total if pedido_item.quantidade > 0 else 0

        return JsonResponse({
            'mensagem': 'Item atualizado!',
            'produto_id': produto.id,
            'quantidade': pedido_item.quantidade if pedido_item.quantidade > 0 else 0,
            'total_produto': total_produto,
            'total_pedido': total_pedido,
            'total_itens': total_itens
        })

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

        # Atualiza o cookie
        response = JsonResponse({})
        response.set_cookie('cart', json.dumps(carrinho))

        # Recalcular os dados do carrinho (como em utils.py)
        try:
            produto = Produto.objects.get(id=produto_id)
        except Produto.DoesNotExist:
            return response

        quantidade = carrinho.get(str(produto_id), {}).get('quantidade', 0)
        total_produto = float(produto.preço) * quantidade
        total_itens = sum(item['quantidade'] for item in carrinho.values())
        total_pedido = 0

        for pid, item in carrinho.items():
            try:
                prod = Produto.objects.get(id=pid)
                total_pedido += float(prod.preço) * item['quantidade']
            except Produto.DoesNotExist:
                continue

        response = JsonResponse({
            'mensagem': 'Item atualizado no carrinho!',
            'produto_id': produto.id,
            'quantidade': quantidade,
            'total_produto': total_produto,
            'total_pedido': total_pedido,
            'total_itens': total_itens,
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



@login_required
@require_POST
def finalizar_compra(request):
    cliente = Customer.objects.get(usuario=request.user)
    pedido = Pedido.objects.filter(cliente=cliente, completo=False).first()

    if not pedido:
        messages.error(request, 'Nenhum pedido em aberto encontrado.')
        return redirect('carrinho')

    # Marca como finalizado
    pedido.completo = True
    pedido.save()

    # (opcional) Redireciona para o perfil com mensagem
    messages.success(request, 'Compra finalizada com sucesso!')
    return redirect('perfil')





def carrinho_quantidade(request):
    dados = carrinhodata(request)
    return JsonResponse({'total_itens': dados['total_itens']})