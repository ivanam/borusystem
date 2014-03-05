from django.conf.urls import patterns, url

urlpatterns = patterns('',

url(r'^$', 'gestiones.Administrador.modificarusuarios.views.modificarusuarios', name="modificarusuarios"),
url(r'^(?P<id_user>\d+)$', 'gestiones.Administrador.modificarusuarios.views.modificarusuarios', name="modificaruser_id"),
url(r'^del/(?P<id_user>\d+)$', 'gestiones.Administrador.modificarusuarios.views.modificaruserdel', name="modificaruser_id_del"),
url(r'^buscar$', 'gestiones.Administrador.modificarusuarios.views.buscaruserajax', name="buscador_user_ajax"),
url(r'^buscarresultados$', 'gestiones.Administrador.modificarusuarios.views.buscaruserajaxResultados', name="buscador_user_ajax_resultados"),
url(r'^paginar', 'gestiones.Administrador.modificarusuarios.views.paginadorajaxResultados', name="paginador_ajax_resultados_user"),
)