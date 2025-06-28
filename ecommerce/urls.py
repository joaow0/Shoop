"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#Criar rotas temporárias para os arquivos da pasta media/
from django.conf.urls.static import static

#Acessar o MEDIA_URL e MEDIA_ROOT
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loja.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#serve para permitir que os arquivos enviados (como imagens) sejam acessados via URL durante o desenvolvimento (modo debug) no Django.
#settings.MEDIA_URL é o prefixo da URL onde os arquivos vão ser acessados, no caso: /imagens/.
#settings.MEDIA_ROOT → é a pasta no seu computador onde esses arquivos realmente estão salvos, por exemplo: media/.
#Durante o desenvolvimento (DEBUG = True), o Django não serve arquivos de mídia automaticamente, então precisa adicionar isso manualmente.
