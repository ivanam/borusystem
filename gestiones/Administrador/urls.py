from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'gestiones.Administrador.views.Administrador', name="administrador"),
url(r'^listarImprimir$', 'gestiones.Administrador.views.listarImprimir', name="listarImprimir"),
url(r'^consulta+vendidos$', 'gestiones.Administrador.views.masVendidos', name="consulta+vendidos"),
url(r'^ayudaContextual$', 'gestiones.Administrador.views.ayudaContextual', name="ayudaContextual"),
url(r'^consultaFacturas$', 'gestiones.Administrador.views.consultaFacturas', name="consultaFacturas"),



)