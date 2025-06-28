from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import cookiecarrinho, carrinhodata, pedidoguest
from django.contrib import messages
from django.db.models import Avg  # importante pra aggregate funcionar sem erro
from random import sample
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from decimal import Decimal
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.utils import timezone



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




def produtoDetalhes(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
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



def registro(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            form.save()  # Cria o User e o Customer via forms.py
            return redirect('login')
    else:
        form = FormRegistro()

    return render(request, 'loja/registro.html', {'form': form})



@login_required
def perfil(request):
    cliente = Customer.objects.get(usuario=request.user)
    pedidos = Pedido.objects.filter(cliente=cliente, completo=True).order_by('-data_pedido')

    contexto = {
        'cliente': cliente,
        'pedidos': pedidos
    }
    return render(request, 'loja/perfil.html', contexto)




@staff_member_required
def dashboard_admin(request):
    pedidos = Pedido.objects.filter(completo=True)
    total_vendas = Decimal('0.00')
    total_pedidos = pedidos.count()
    total_itens_vendidos = 0

    for pedido in pedidos:
        total_vendas += pedido.get_cart_total
        total_itens_vendidos += pedido.get_cart_items

    produtos_mais_vendidos = (
        PedidoItem.objects.filter(pedido__completo=True)
        .values('produto__nome')
        .annotate(total_vendido=Sum('quantidade'))
        .order_by('-total_vendido')[:10]
    )

    total_estoque = Produto.objects.aggregate(total=Sum('estoque'))['total'] or 0

    contexto = {
        'total_vendas': total_vendas,
        'total_pedidos': total_pedidos,
        'total_itens_vendidos': total_itens_vendidos,
        'produtos_mais_vendidos': produtos_mais_vendidos,
        'total_estoque': total_estoque,
    }

    return render(request, 'loja/dashboard_admin.html', contexto)




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






@staff_member_required
def exportar_csv(request):
    filtro = request.GET.get('filtro', '7')
    hoje = timezone.now().date()

    if filtro == '7':
        data_inicio = hoje - timedelta(days=7)
    elif filtro == '30':
        data_inicio = hoje - timedelta(days=30)
    elif filtro == 'mes':
        data_inicio = hoje.replace(day=1)
    else:
        data_inicio = None  # todos

    pedidos = Pedido.objects.filter(completo=True)
    if data_inicio:
        pedidos = pedidos.filter(data_pedido__gte=data_inicio)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_vendas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Data', 'Cliente', 'Produto', 'Quantidade', 'Preço Unitário', 'Total'])

    for pedido in pedidos:
        for item in pedido.pedidoitem_set.all():
            writer.writerow([
                pedido.data_pedido.strftime('%d/%m/%Y'),
                pedido.cliente.nome if pedido.cliente else 'N/A',
                item.produto.nome if item.produto else 'N/A',
                item.quantidade,
                f'{item.produto.preço:.2f}' if item.produto else '0.00',
                f'{item.get_total:.2f}'
            ])

    return response