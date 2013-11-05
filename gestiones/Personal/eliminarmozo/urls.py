from django.conf.urls import patterns, include, url
from .views import eliminarmozo, eliminarmozoFiltro
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    
url(r'^$',eliminarmozo.as_view(),name = "eliminarmozo"),
url(r'^filtrar/$','gestiones.Personal.eliminarmozo.views.eliminarmozoFiltro',name = "eliminarmozofiltro"),
url(r'^del/(?P<id_user>\d+)$', 'gestiones.Personal.eliminarmozo.views.eliminarmozodel',
                           name="eliminar_mozo_id"),
url(r'^buscar$', 'gestiones.Personal.eliminarmozo.views.buscarmozoajax',
                           name="buscador_mozo_ajax"),
)