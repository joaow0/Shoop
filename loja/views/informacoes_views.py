from django.shortcuts import render

def termos(request):
    return render(request, 'loja/termos.html')


def sobre(request):
    return render(request, 'loja/sobre.html')

def contato(request):
    return render(request, 'loja/contato.html')

