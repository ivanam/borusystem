from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

                      url(r'^$', 'gestiones.Producto.modificarmenudia.views.modificarmenudia', name="modificarmenudia"),
                      url(r'^(?P<id_menu>\d+)$', 'gestiones.Producto.modificarmenudia.views.modificarmenudia',
                           name="modificarmenu_id"),
                      url(r'^del/(?P<id_menu>\d+)$', 'gestiones.Producto.modificarmenudia.views.modificarmenudel',
                           name="modificarmenu_id_del"),
                      url(r'^agregar', 'gestiones.Producto.modificarmenudia.views.agregarProductoListaAjax',
                          name="agregar_producto_lista_ajax_mdm"),

)