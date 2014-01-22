from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.stockbebida.views.stockbebida', name="stockbebida"),
                       url(r'^(?P<id_bebida>\d+)$', 'gestiones.Producto.stockbebida.views.stockbebida',
                           name="stockbebida_id"),



                       url(r'^buscar$', 'gestiones.Producto.stockbebida.views.buscarbebidasajax',
                           name="buscador_bebidas_ajax"),

                       url(r'^buscarresultados$', 'gestiones.Producto.stockbebida.views.buscarbebidasajaxResultados',
                           name="buscador_bebidas_ajax_resultados"),

                       url(r'^paginar', 'gestiones.Producto.stockbebida.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_bebidas"),


)


