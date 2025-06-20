# utils.py

import json
from .models import Customer, Produto, Pedido, PedidoItem

def cookiecarrinho(request):
    try:
        carrinho = json.loads(request.COOKIES.get('cart', '{}'))
    except:
        carrinho = {}

    itens = []
    pedido = {'get_total_carrinho': 0, 'get_total_itens': 0, 'envio': False}
    carrinhoitens = 0

    for prod_id, info in carrinho.items():
        try:
            quantidade = info.get('quantidade', 0)
            produto = Produto.objects.get(id=prod_id)
            total = produto.preço * quantidade

            carrinhoitens += quantidade
            pedido['get_total_carrinho'] += total
            pedido['get_total_itens'] += quantidade

            itens.append({
                'produto': {
                    'id': produto.id,
                    'nome': produto.nome,
                    'preço': produto.preço,
                    'imagemURL': produto.imagem.url,
                },
                'quantidade': quantidade,
                'get_total': total,
            })

            if not produto.digital:
                pedido['envio'] = True

        except Produto.DoesNotExist:
            continue

    return {'carrinhoitens': carrinhoitens, 'pedido': pedido, 'itens': itens}


def carrinhodata(request):
    if request.user.is_authenticated:
        # Pega o Customer (assumindo OneToOne User→Customer)
        cliente = Customer.objects.get(usuario=request.user)

        # Busca o pedido incompleto mais recente, ou cria um novo
        pedido = (Pedido.objects
                  .filter(cliente=cliente, completo=False)
                  .order_by('-id')
                  .first())
        if not pedido:
            pedido = Pedido.objects.create(cliente=cliente, completo=False)

        itens = pedido.pedidoitem_set.all()
        carrinhoitens = pedido.get_cart_items

    else:
        cookiedata = cookiecarrinho(request)
        carrinhoitens = cookiedata['carrinhoitens']
        pedido = cookiedata['pedido']
        itens = cookiedata['itens']

    return {'carrinhoitens': carrinhoitens, 'pedido': pedido, 'itens': itens}


def pedidoguest(request, data):
    nome = data['form'].get('nome')
    email = data['form'].get('email')

    cookiedata = cookiecarrinho(request)
    itens = cookiedata['itens']

    customer, criado = Customer.objects.get_or_create(
        email=email,
        defaults={'nome': nome}
    )
    if not criado:
        customer.nome = nome
        customer.save()

    pedido = Pedido.objects.create(cliente=customer, completo=False)

    for item in itens:
        produto = Produto.objects.get(id=item['produto']['id'])
        PedidoItem.objects.create(
            produto=produto,
            pedido=pedido,
            quantidade=item['quantidade']
        )

    return customer, pedido
