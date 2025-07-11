from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .forms import EmailAuthenticationForm

urlpatterns = [
    path('', views.loja, name='loja'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('atualizacaoitem/', views.atualizacaoitem, name='atualizacaoitem'),
    path('pedidoProcesso/', views.pedidoProcesso, name='pedidoProcesso'),
    path('produto/<int:pk>/', views.produtoDetalhes, name='produto'),
    path('produtoDetalhes/', views.produtoDetalhes, name='produtoDetalhes'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('login/', auth_views.LoginView.as_view(
        template_name='loja/login.html', authentication_form=EmailAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='loja'), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('admin-dashboard/', views.dashboard_admin, name='admin_dashboard'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('exportar-csv/', views.exportar_csv, name='exportar_csv'),
    path('produto/<slug:slug>/', views.produtoDetalhes, name='produto'),
    path('categoria/<str:categoria_slug>/', views.produtos_por_categoria, name='produtos_por_categoria'),
    path('sobre/', views.sobre, name='sobre'),
    path('termos/', views.termos, name='termos'),
    path('contato/', views.contato, name='contato'),
    path('ofertas/', views.ofertas, name='ofertas'), 
    path('carrinho/quantidade/', views.carrinho_quantidade, name='carrinho_quantidade'),
]