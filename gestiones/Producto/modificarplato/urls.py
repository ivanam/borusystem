from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', "gestiones.Producto.modificarplato.views.modificarplato", name="modificarplato"),
                       url(r'^(?P<id_plato>\d+)$', 'gestiones.Producto.modificarplato.views.modificarplato',
                           name="modificarplato_id"),
                       url(r'^del/(?P<id_plato>\d+)$', 'gestiones.Producto.modificarplato.views.modificarplatodel',
                           name="modificarplato_id_del"),


                       url(r'^buscar$', 'gestiones.Producto.modificarplato.views.buscarproductoajax',
                           name="buscador_producto_ajax_mod"),

                       url(r'^buscarresultados$', 'gestiones.Producto.modificarplato.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados_mod"),

                       url(r'^paginar', 'gestiones.Producto.modificarplato.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_mod"),


)
