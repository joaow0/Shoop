from django.contrib import admin
from .models import *

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoInline]
    fields = [
        'nome',
        'preço',
        'digital',
        'imagem',
        'descricao',         # 🛒 "Sobre este produto"
        'caracteristicas',   # 🔧 Características Técnicas
        'categoria',
        'estoque',
    ]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'email', 'cpf_cnpj', 'telefone_celular', 'data_cadastro']
    search_fields = ['usuario__username', 'cpf_cnpj', 'email', 'telefone_celular']
    list_filter = ['genero', 'cidade', 'estado', 'data_cadastro']
    readonly_fields = ['data_cadastro']
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('usuario', 'email', 'cpf_cnpj', 'rg', 'data_nascimento', 'genero')
        }),
        ('Contato', {
            'fields': ('telefone_celular', 'telefone_fixo')
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep')
        }),
        ('Outros', {
            'fields': ('preferencias', 'data_cadastro')
        }),
    )

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(EndereçoEnvio)
admin.site.register(Avaliacao)
