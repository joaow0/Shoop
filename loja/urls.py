from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('atualizacaoitem/', views.atualizacaoitem, name='atualizacaoitem'),
    path('pedidoProcesso/', views.pedidoProcesso, name='pedidoProcesso'),
    path('produto/<int:pk>/', views.produtoDetalhes, name='produto'),
    path('produtoDetalhes/', views.produtoDetalhes, name='produtoDetalhes'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
]
