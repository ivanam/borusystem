from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.modificarbebida.views.modificarbebida', name="modificarbebida"),
                       url(r'^(?P<id_bebida>\d+)$', 'gestiones.Producto.modificarbebida.views.modificarbebida',
                           name="modificarbebida_id"),
                       url(r'^del/(?P<id_bebida>\d+)$', 'gestiones.Producto.modificarbebida.views.modificarbebidadel',
                           name="modificarbebida_id_del"),


                       url(r'^buscar$', 'gestiones.Producto.modificarbebida.views.buscarbebidasajax',
                           name="buscador_bebidas_ajax"),

                       url(r'^buscarresultados$', 'gestiones.Producto.modificarbebida.views.buscarbebidasajaxResultados',
                           name="buscador_bebidas_ajax_resultados"),

                       url(r'^paginar', 'gestiones.Producto.modificarbebida.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_bebidas"),


)


