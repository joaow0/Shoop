from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(EndereçoEnvio)
admin.site.register(Avaliacao) 
#dessa forma que se adiciona as models no admin do site


