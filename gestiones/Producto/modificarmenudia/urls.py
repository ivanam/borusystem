from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

                      url(r'^$', 'gestiones.Producto.modificarmenudia.views.modificarmenudia', name="modificarmenudia"),
                      url(r'^(?P<id_menu>\d+)$', 'gestiones.Producto.modificarmenudia.views.modificarmenudia',
                           name="modificarmenu_id"),
                      url(r'^del/(?P<id_menu>\d+)$', 'gestiones.Producto.modificarmenudia.views.modificarmenudel',
                           name="modificarmenu_id_del"),

)