from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.altamenudia.views.altamenudia', name="altamenudia"),
                       url(r'^buscar$', 'gestiones.Producto.altamenudia.views.buscarproductoajax',
                           name="buscador_producto_ajax"),
                       url(r'^buscarresultados$', 'gestiones.Producto.altamenudia.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados"),
                       url(r'^agregar', 'gestiones.Producto.altamenudia.views.agregarProductoListaAjax',
                           name="agregar_producto_lista_ajax"),
                       url(r'^paginar', 'gestiones.Producto.altamenudia.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados"),



)