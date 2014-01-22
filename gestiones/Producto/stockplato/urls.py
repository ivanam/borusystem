from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', "gestiones.Producto.stockplato.views.stockplato", name="stockplato"),
                       url(r'^(?P<id_plato>\d+)$', 'gestiones.Producto.stockplato.views.stockplato',
                           name="stockplato_id"),

)
