from loja.utils import carrinhodata
from loja.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from random import sample
from django.db.models import Avg
from django.contrib import messages
from django.http import Http404
from decimal import Decimal

def loja(request):
    data = carrinhodata(request)
    carrinhoitens = data['carrinhoitens']

    todos_produtos = Produto.objects.all().order_by('nome')
    paginator = Paginator(todos_produtos, 12)  # 12 produtos por página (ajuste se quiser)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    contexto = {
        'produtos': produtos,
        'carrinhoitens': carrinhoitens,
    }
    return render(request, 'loja/loja.html', contexto)




def produtoDetalhes(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    avaliacoes = Avaliacao.objects.filter(produto=produto)
    media = avaliacoes.aggregate(Avg('nota'))['nota__avg'] or 0
    media = round(media, 1)
    data = carrinhodata(request)
    outros_produtos = Produto.objects.exclude(id=produto.id)
    recomendados = sample(list(outros_produtos), min(4, outros_produtos.count()))

    if request.method == 'POST':
        if request.user.is_authenticated:
            cliente = Customer.objects.get(usuario=request.user)
            nota = int(request.POST.get('nota'))
            comentario = request.POST.get('comentario', '')

            avaliacao, created = Avaliacao.objects.get_or_create(
                cliente=cliente,
                produto=produto,
                defaults={'nota': nota, 'comentario': comentario}
            )

            if not created:
                messages.error(request, 'Você já avaliou este produto.')
            else:
                messages.success(request, 'Avaliação enviada com sucesso!')

            return redirect('produto', slug=produto.slug)
        else:
            messages.error(request, 'Você precisa estar logado para avaliar.')
            return redirect(f'/login/?next=/produto/{produto.slug}/')

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



def produtos_por_categoria(request, categoria_slug):
    data = carrinhodata(request)
    carrinhoitens = data['carrinhoitens']

    produtos_lista = Produto.objects.filter(categoria=categoria_slug)

    categorias_disponiveis = [slug for slug, _ in Produto.CATEGORIAS]
    if categoria_slug not in categorias_disponiveis:
        raise Http404("Categoria não encontrada.")

    categoria_selecionada_nome = categoria_slug

    ordenacao = request.GET.get('ordenar', '')
    preco_min = request.GET.get('preco_min', '')
    preco_max = request.GET.get('preco_max', '')
    tipo_roupa_selecionado = request.GET.get('tipo_roupa', '')
    tipo_acessorio_selecionado = request.GET.get('tipo_acessorio', '')

    # --- LÓGICA DE APLICAÇÃO DE FILTROS ESPECÍFICOS ---
    if categoria_slug == 'roupas':
        if tipo_roupa_selecionado:
            produtos_lista = produtos_lista.filter(tipo_roupa=tipo_roupa_selecionado)
        # O filtro de tipo_acessorio NÃO é aplicado aqui
        tipo_acessorio_selecionado = '' # Garante que a seleção de acessório seja resetada

    elif categoria_slug == 'acessorios':
        if tipo_acessorio_selecionado:
            produtos_lista = produtos_lista.filter(tipo_acessorio=tipo_acessorio_selecionado)
        tipo_roupa_selecionado = ''
    else: # Para todas as outras categorias
        tipo_roupa_selecionado = ''
        tipo_acessorio_selecionado = ''
    
    # --- Lógica de filtragem por preço (mantida) ---
    if preco_min:
        try:
            produtos_lista = produtos_lista.filter(preço__gte=Decimal(preco_min))
        except:
            pass
    if preco_max:
        try:
            produtos_lista = produtos_lista.filter(preço__lte=Decimal(preco_max))
        except:
            pass

    # --- Lógica de ordenação (mantida) ---
    if ordenacao == 'menor_preco':
        produtos_lista = produtos_lista.order_by('preço')
    elif ordenacao == 'maior_preco':
        produtos_lista = produtos_lista.order_by('-preço')
    elif ordenacao == 'a_z':
        produtos_lista = produtos_lista.order_by('nome')
    elif ordenacao == 'z_a':
        produtos_lista = produtos_lista.order_by('-nome')
    else:
        produtos_lista = produtos_lista.order_by('nome')

    paginator = Paginator(produtos_lista, 25)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    categorias_disponiveis = Produto.CATEGORIAS 

    contexto = {
        'produtos': produtos,
        'carrinhoitens': carrinhoitens,
        'categoria_selecionada': categoria_selecionada_nome,
        'ordenacao': ordenacao,
        'preco_min': preco_min,
        'preco_max': preco_max,
        'categorias_disponiveis': categorias_disponiveis,
    }

    # --- Passagem de contexto para os filtros de Tipo de Roupa/Acessório ---
    if categoria_slug == 'roupas':
        contexto['tipo_roupa_selecionado'] = tipo_roupa_selecionado
        contexto['tipos_roupa_choices'] = Produto.TIPOS_ROUPA
        # Não passa nada para 'tipo_acessorio_selecionado' e 'tipos_acessorios_choices'

    elif categoria_slug == 'acessorios':
        contexto['tipo_roupa_selecionado'] = ''
        contexto['tipo_acessorio_selecionado'] = tipo_acessorio_selecionado
        contexto['tipos_roupa_choices'] = []
        contexto['tipos_acessorios_choices'] = Produto.TIPOS_ACESSORIOS

    
    else: # Para todas as outras categorias, garante que as variáveis existam, mas vazias
        contexto['tipo_roupa_selecionado'] = ''
        contexto['tipo_acessorio_selecionado'] = ''
        contexto['tipos_roupa_choices'] = []
        contexto['tipos_acessorios_choices'] = []

    return render(request, 'loja/produtos_por_categoria.html', contexto)



def ofertas(request):
    produtos_em_oferta = Produto.objects.filter(preco_desconto__isnull=False).exclude(preco_desconto=0)
    paginator = Paginator(produtos_em_oferta, 12)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    return render(request, 'loja/ofertas.html', {'produtos': produtos})


