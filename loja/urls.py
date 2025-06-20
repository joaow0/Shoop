from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('atualizaçãoitem/', views.atualizaçãoitem, name='atualizaçãoitem'),
    path('pedidoProcesso/', views.pedidoProcesso, name='pedidoProcesso'),
]
