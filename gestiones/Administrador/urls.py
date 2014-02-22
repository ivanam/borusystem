from django.conf.urls import patterns, include, url
from .views import Administrador
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    
url(r'^$', 'gestiones.Administrador.views.Administrador', name="administrador"),

url(r'^listarImprimir$', 'gestiones.Administrador.views.listarImprimir', name="listarImprimir"),
url(r'^consulta+vendidos$', 'gestiones.Administrador.views.masVendidos', name="consulta+vendidos"),

url(r'^ayudaContextual$', 'gestiones.Administrador.views.ayudaContextual', name="ayudaContextual"),

#url(r'^pruebaUsuario$', 'gestiones.Administrador.views.PruebaUsuario', name="pruebaUsuario"),
#url(r'^altaAdministrador$', 'gestiones.Administrador.views.AltaAdministrador', name="altaAdministrador"),
#url(r'^pruebaUsuario$', 'gestiones.Administrador.views.PruebaUsuario', name="usuario"),

)