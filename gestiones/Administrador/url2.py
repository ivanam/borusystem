from django.conf.urls import patterns, include, url
from .views import Administrador
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

#url(r'^pruebaUsuario$', 'gestiones.Administrador.views.PruebaUsuario', name="pruebaUsuario"),
url(r'^$', 'gestiones.Administrador.views.AltaAdministrador', name="altaAdministrador"),
#url(r'^pruebaUsuario$', 'gestiones.Administrador.views.PruebaUsuario', name="usuario"),

)
