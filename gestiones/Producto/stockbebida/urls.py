from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', "gestiones.Producto.stockbebida.views.stockbebida", name="stockbebida"),

                       url(r'^(?P<id_plato>\d+)$', 'gestiones.Producto.stockbebida.views.stockbebida',
                           name="stockbebida_id"),

                       url(r'^del/(?P<id_plato>\d+)$', 'gestiones.Producto.stockbebida.views.modificarbebidadel',
                           name="stockbebida_id_del"),

                       url(r'^buscar$', 'gestiones.Producto.stockbebida.views.buscarproductoajax',
                           name="buscador_producto_ajax_stockb"),

                       url(r'^buscarresultados$', 'gestiones.Producto.stockbebida.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados_stockb"),

                       url(r'^paginar', 'gestiones.Producto.stockbebida.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_stockb"),

)
