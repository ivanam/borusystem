from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.altamenuejecutivo.views.altamenuejecutivo', name="altamenuejecutivo"),
                        url(r'^buscar$', 'gestiones.Producto.altamenuejecutivo.views.buscarproductoajax',
                           name="buscador_producto_ajax"),
                       url(r'^buscarresultados$', 'gestiones.Producto.altamenuejecutivo.views.buscarproductoajaxResultados',
                           name="buscador_producto_ajax_resultados"),
                       url(r'^agregar', 'gestiones.Producto.altamenuejecutivo.views.agregarProductoListaAjax',
                           name="agregar_producto_lista_ajax"),
                       url(r'^paginar', 'gestiones.Producto.altamenuejecutivo.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados"),

)