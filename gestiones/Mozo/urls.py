from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Mozo.views.inicio', name="mozo"),
                       url(r'^comanda$', 'gestiones.Mozo.views.crearcomanda', name="crearcomanda"),
                       url(r'^productos$', 'gestiones.Mozo.views.seleccionarproductos', name="seleccionarproductos"),
                       url(r'^cargarproductos$', 'gestiones.Mozo.views.cargararproductosajax', name="cargarproductosajax"),
                       url(r'^cargarmesas$', 'gestiones.Mozo.views.cargararmesasjax', name="cargararmesasjax"),
                       url(r'^sacarmesas$', 'gestiones.Mozo.views.sacarmesasjax', name="sacarmesasjax"),
                       url(r'^guardarproducto$', 'gestiones.Mozo.views.guardarproductosajax', name="guardarproductosajax"),
                       url(r'^cargar$', 'gestiones.Mozo.views.cargarpanelajax', name="cargarpanelajax"),
                       url(r'^cancelarComanda$', 'gestiones.Mozo.views.cancelarComandajax', name="cancelarComandajax"),
                       url(r'^finalizar$', 'gestiones.Mozo.views.finalizar', name="finalizar"),
                       url(r'^volvermesas$', 'gestiones.Mozo.views.vistaMesas', name="vistaMesas"),
                       url(r'^guardarComanda$', 'gestiones.Mozo.views.guardarComanda', name="guardarComanda"),

                       url(r'^eliminarproductos', 'gestiones.Mozo.views.eliminarProductosAjaxSeleccionado', name="eliminar_producto_ajax_seleccionado"),
                       url(r'^miscomandas/(?P<pagina>\d+)*', 'gestiones.Mozo.views.miscomandas',name="miscomandas"),


                       url(r'^detalle$', 'gestiones.Mozo.views.detalle_comanda_ajax', name="detalle_comanda_ajax_mozo"),

                       url(r'^detalle_preticket$', 'gestiones.Mozo.views.detalle_preticket_ajax',
                           name="detalle_preticket_ajax_mozo"),

                       url(r'^detalle_factura$', 'gestiones.Mozo.views.detalle_factura_ajax',
                           name="detalle_factura_ajax_mozo"),

                       url(r'^cerrar_comanda/(?P<id_comanda>\d+)$', 'gestiones.Mozo.views.cerrar_comanda',
                           name="cerrar_comanda_mozo"),

                       url(r'^una_comanda/(?P<id_comanda>\d+)$', 'gestiones.Mozo.views.una_comanda',
                           name="una_comanda_mozo"),

                       url(r'^editar_detalle_comanda$', 'gestiones.Mozo.views.editar_detalle_comanda_ajax',
                           name="editar_detalle_comanda_ajax"),


                       url(r'^guardar_detalle_comanda$', 'gestiones.Mozo.views.guardar_detalle_comanda_ajax',
                           name="guardar_detalle_comanda_ajax"),

                       url(r'^buscar$', 'gestiones.Mozo.views.buscarproductoajax', name="buscador_producto_ajax_mozo"),

                       url(r'^buscarresultados$', 'gestiones.Mozo.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados_mozo"),


)