from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^(?P<pagina>\d+)*$', 'gestiones.Cajero.views.Cajero', name="cajero"),
    url(r'^detalle$', 'gestiones.Cajero.views.detalle_comanda_ajax', name="detalle_comanda_ajax"),
    url(r'^pedidos$', 'gestiones.Cajero.views.pedidos_pub', name="pedidos_pub"),
    url(r'^polling', 'gestiones.Cajero.views.polling_comandas', name="polling_comandas"),
    url(r'^ver_comanda', 'gestiones.Cajero.views.comanda_vista', name="comanda_vista"),

)