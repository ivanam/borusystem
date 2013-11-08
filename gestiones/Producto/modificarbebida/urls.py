from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.modificarbebida.views.modificarbebida', name="modificarbebida"),
                       url(r'^(?P<id_bebida>\d+)$', 'gestiones.Producto.modificarbebida.views.modificarbebida',
                           name="modificarbebida_id"),
                       url(r'^del/(?P<id_bebida>\d+)$', 'gestiones.Producto.modificarbebida.views.modificarbebidadel',
                           name="modificarbebida_id_del"),
)


