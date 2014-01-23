from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', "gestiones.Producto.stockplato.views.stockplato", name="stockplato"),
                       url(r'^(?P<id_plato>\d+)$', 'gestiones.Producto.stockplato.views.stockplato',
                           name="stockplato_id"),
                       url(r'^del/(?P<id_plato>\d+)$', 'gestiones.Producto.stockplato.views.modificarplatodel',
                           name="stockplato_id_del"),



                       url(r'^buscar$', 'gestiones.Producto.stockplato.views.buscarproductoajax',
                           name="buscador_producto_ajax_mod"),

                       url(r'^buscarresultados$', 'gestiones.Producto.stockplato.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados_mod"),

                       url(r'^paginar', 'gestiones.Producto.stockplato.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_mod"),


)
