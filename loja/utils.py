import json
from .models import Customer, Produto, Pedido, PedidoItem


def cookiecarrinho(request):
    try:
        carrinho = json.loads(request.COOKIES.get('cart', '{}'))
    except:
        carrinho = {}

    itens = []
    pedido = {'get_cart_total': 0, 'get_cart_items': 0, 'envio': False}
    carrinhoitens = 0

    for prod_id, info in carrinho.items():
        try:
            quantidade = info.get('quantidade', 0)
            produto = Produto.objects.get(id=prod_id)
            total = produto.preço * quantidade

            carrinhoitens += quantidade
            pedido['get_cart_total'] += total
            pedido['get_cart_items'] += quantidade

            itens.append({
                'produto': {
                    'id': produto.id,
                    'nome': produto.nome,
                    'preço': produto.preço,
                    'imagemURL': produto.imagemURL,
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
        cliente, _ = Customer.objects.get_or_create(
            usuario=request.user,
            defaults={'nome': request.user.username, 'email': request.user.email}
        )
        pedido, _ = Pedido.objects.get_or_create(cliente=cliente, completo=False)

        # ⚠️ Limpa primeiro os produtos deletados
        pedido.pedidoitem_set.filter(produto__isnull=True).delete()

        try:
            carrinhoitens = pedido.get_cart_items
            itens = pedido.pedidoitem_set.all()
        except Exception as e:
            print(f"[ERRO] carrinho: {e}")
            carrinhoitens = 0
            itens = []

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
