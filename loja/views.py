from django.shortcuts import render
from .models import Customer, Pedido, PedidoItem, Produto, EndereçoEnvio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from .utils import cookiecarrinho, carrinhodata, pedidoguest


def loja(request):
    data = carrinhodata(request)
    data['produtos'] = Produto.objects.all()
    return render(request, 'loja/loja.html', data)


def carrinho(request):
    data = carrinhodata(request)
    return render(request, 'loja/carrinho.html', data)


def checkout(request):
    data = carrinhodata(request)
    return render(request, 'loja/checkout.html', data)


def atualizaçãoitem(request):
    data = json.loads(request.body)
    cliente = Customer.objects.get(usuario=request.user)
    produto = Produto.objects.get(id=data['productId'])

    pedido = (Pedido.objects
              .filter(cliente=cliente, completo=False)
              .order_by('-id')
              .first())
    if not pedido:
        pedido = Pedido.objects.create(cliente=cliente, completo=False)

    pedidoitem, criado = PedidoItem.objects.get_or_create(
        pedido=pedido, produto=produto)

    if data['action'] == 'add':
        pedidoitem.quantidade += 1
    else:
        pedidoitem.quantidade -= 1
    pedidoitem.save()
    if pedidoitem.quantidade <= 0:
        pedidoitem.delete()

    return JsonResponse('item adicionado', safe=False)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def pedidoProcesso(request):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            cliente = Customer.objects.get(usuario=request.user)
            pedido = (Pedido.objects
                      .filter(cliente=cliente, completo=False)
                      .order_by('-id')
                      .first())
            if not pedido:
                pedido = Pedido.objects.create(cliente=cliente, completo=False)
        else:
            cliente, pedido = pedidoguest(request, data)

        total = float(data['form'].get('total', 0))
        pedido.transaction_id = transaction_id
        if total == float(pedido.get_cart_total):
            pedido.completo = True
        pedido.save()

        if pedido.envio:
            envio = data.get('envio', {})
            EndereçoEnvio.objects.create(
                cliente=cliente,
                pedido=pedido,
                endereço=envio.get('address', ''),
                cidade=envio.get('city', ''),
                estado=envio.get('state', ''),
                cep=envio.get('zipcode', ''),
            )

        # Limpar cookie de carrinho completamente
        response = JsonResponse('Pagamento concluído!', safe=False)
        response.delete_cookie('cart', path='/')
        return response
