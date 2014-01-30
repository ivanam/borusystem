from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

                      url(r'^$', 'gestiones.Producto.modificarmenuejecutivo.views.modificarmenuejecutivo', name="modificarmenuejecutivo"),
                      url(r'^(?P<id_menu>\d+)$', 'gestiones.Producto.modificarmenuejecutivo.views.modificarmenuejecutivo',
                           name="modificarmenu_id_eje"),
                      url(r'^del/(?P<id_menu>\d+)$', 'gestiones.Producto.modificarmenuejecutivo.views.modificarmenudel',
                           name="modificarmenu_id_del_eje"),

                      url(r'^agregar', 'gestiones.Producto.modificarmenuejecutivo.views.agregarProductoListaAjax',
                          name="agregar_producto_lista_ajax_eje"),

                      url(r'^paginar', 'gestiones.Producto.modificarmenuejecutivo.views.paginadorajaxResultados',
                          name="paginador_ajax_resultados_eje"),
                      url(r'^buscar$', 'gestiones.Producto.modificarmenuejecutivo.views.buscarproductoajax',
                          name="buscador_producto_ajax_eje"),
                      url(r'^buscarresultados$', 'gestiones.Producto.modificarmenuejecutivo.views.buscarproductoajaxResultados',
                          name="buscador_producto_ajax_resultados_eje"),

                      url(r'^borraSesion', 'gestiones.Producto.modificarmenuejecutivo.views.borrarSesionAjax',
                          name="borrarSesionAjax_eje"),


)