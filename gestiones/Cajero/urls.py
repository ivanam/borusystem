from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^$', 'gestiones.Cajero.views.Cajero', name="cajero"),
    url(r'^detalle$', 'gestiones.Cajero.views.detalle_comanda_ajax', name="detalle_comanda_ajax"),
    url(r'^pedidos$', 'gestiones.Cajero.views.pedidos_pub', name="pedidos_pub"),
)