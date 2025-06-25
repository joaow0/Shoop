from django.contrib import admin
from .models import *



class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoInline]

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Customer)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(EndereçoEnvio)
admin.site.register(Avaliacao)
#dessa forma que se adiciona as models no admin do site

