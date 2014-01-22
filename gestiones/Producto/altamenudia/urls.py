from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.altamenudia.views.altamenudia', name="altamenudia"),
                       url(r'^buscar$', 'gestiones.Producto.altamenudia.views.buscarproductoajax',
                           name="buscador_producto_ajax_md"),
                       url(r'^buscarresultados$', 'gestiones.Producto.altamenudia.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados_md"),
                       url(r'^agregar', 'gestiones.Producto.altamenudia.views.agregarProductoListaAjax',
                           name="agregar_producto_lista_ajax_md"),
                       url(r'^paginar', 'gestiones.Producto.altamenudia.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_md"),
)