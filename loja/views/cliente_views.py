from django.contrib.auth.decorators import login_required
from loja.models import *
from django.shortcuts import render, redirect
from loja.forms import FormRegistro

@login_required
def perfil(request):
    cliente = Customer.objects.get(usuario=request.user)
    pedidos = Pedido.objects.filter(cliente=cliente, completo=True).order_by('-data_pedido')

    contexto = {
        'cliente': cliente,
        'pedidos': pedidos
    }
    return render(request, 'loja/perfil.html', contexto)


def registro(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            form.save()  # Cria o User e o Customer via forms.py
            return redirect('login')
    else:
        form = FormRegistro()

    return render(request, 'loja/registro.html', {'form': form})

