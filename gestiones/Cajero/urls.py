from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^(?P<pagina>\d+)*$', 'gestiones.Cajero.views.Cajero', name="cajero"),

    url(r'^detalle$', 'gestiones.Cajero.views.detalle_comanda_ajax', name="detalle_comanda_ajax"),

    url(r'^pretickets/(?P<pretickets_page>\d+)*$', 'gestiones.Cajero.views.pretickets', name="pretickets"),

    url(r'^detalle_preticket$', 'gestiones.Cajero.views.detalle_preticket_ajax', name="detalle_preticket_ajax"),

    url(r'^detalle_factura$', 'gestiones.Cajero.views.detalle_factura_ajax', name="detalle_factura_ajax"),

    url(r'^pedidos/(?P<pedidos_page>\d+)*$', 'gestiones.Cajero.views.pedidos_pub', name="pedidos_pub"),

    url(r'^polling', 'gestiones.Cajero.views.polling_comandas', name="polling_comandas"),

    url(r'^ver_comanda', 'gestiones.Cajero.views.comanda_vista', name="comanda_vista"),

    url(r'^cerrar_comanda/(?P<id_comanda>\d+)$', 'gestiones.Cajero.views.cerrar_comanda', name="cerrar_comanda"),

    url(r'^pagar_factura/(?P<id_factura>\d+)/(?P<id_comanda>\d+)$', 'gestiones.Cajero.views.pagar_factura', name="pagar_factura"),

    url(r'^generar_preticket/(?P<id_comanda>\d+)$', 'gestiones.Cajero.views.generar_preticket', name="generar_preticket"),

    url(r'^generar_factura/(?P<id_preticket>\d+)/(?P<id_comanda>\d+)$', 'gestiones.Cajero.views.generar_factura', name="generar_factura"),

    url(r'^buscar_mesa$', 'gestiones.Cajero.views.buscar_mesa', name="buscar_mesa"),

    url(r'^una_comanda/(?P<id_comanda>\d+)$', 'gestiones.Cajero.views.una_comanda', name="una_comanda"),

    url(r'^editar_detalle_preticket$', 'gestiones.Cajero.views.editar_detalle_preticket_ajax', name="editar_detalle_preticket_ajax"),

    url(r'^guardar_detalle_preticket$', 'gestiones.Cajero.views.guardar_detalle_preticket_ajax', name="guardar_detalle_preticket_ajax"),

    url(r'^buscar$', 'gestiones.Cajero.views.buscarproductoajax', name="buscador_producto_ajax_pre"),

    url(r'^buscarresultados$', 'gestiones.Cajero.views.buscarproductoajaxResultados', name="buscador_producto_ajax_resultados_pre"),

    url(r'^facturas/(?P<facturas_page>\d+)*$', 'gestiones.Cajero.views.facturas', name="facturas"),
)