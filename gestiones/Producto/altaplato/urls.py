from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', "gestiones.Producto.altaplato.views.altaplato", name="altaplato"),
)
