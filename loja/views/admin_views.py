from django.shortcuts import render
from loja.models import *
from django.utils import timezone
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta
from django.http import HttpResponse
from django.db.models import Sum
import csv



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


