from django.conf.urls import patterns, include, url
from .views import Administrador
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

url(r'^$', 'gestiones.Administrador.views.ModificarUsuario', name="modificarUsuarios"),

url(r'^(?P<id_user>\d+)$', 'gestiones.Administrador.views.ModificarUsuario',
       name="modificarUsuarios_id"),

url(r'^del/(?P<id_user>\d+)$', 'gestiones.Administrador.views.modificarUsuariodel',
       name="modificarUsuarios_id_del"),

url(r'^buscarresultados$', 'gestiones.Administrador.views.buscarUsuariosajaxResultados',
        name="buscador_usuarios_ajax_resultados"),

url(r'^buscar$', 'gestiones.Administrador.views.buscarUsuariosajax',
        name="buscador_usuarios_ajax"),

url(r'^paginar', 'gestiones.Administrador.views.paginadorajaxResultados',
        name="paginador_ajax_resultados_usuarios"),

)