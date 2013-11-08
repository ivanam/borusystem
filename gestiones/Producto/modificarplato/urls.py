from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', "gestiones.Producto.modificarplato.views.modificarplato", name="modificarplato"),
                       url(r'^(?P<id_plato>\d+)$', 'gestiones.Producto.modificarplato.views.modificarplato',
                           name="modificarplato_id"),
                       url(r'^del/(?P<id_plato>\d+)$', 'gestiones.Producto.modificarplato.views.modificarplatodel',
                           name="modificarplato_id_del"),
)
