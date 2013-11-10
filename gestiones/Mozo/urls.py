from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Mozo.views.inicio', name="mozo"),
                       url(r'^comanda$', 'gestiones.Mozo.views.crearcomanda', name="crearcomanda"),
                       url(r'^productos$', 'gestiones.Mozo.views.seleccionarproductos', name="seleccionarproductos"),
                       url(r'^cargarproductos$', 'gestiones.Mozo.views.cargararproductosajax', name="cargarproductosajax"),
)