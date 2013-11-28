from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Mozo.views.inicio', name="mozo"),
                       url(r'^comanda$', 'gestiones.Mozo.views.crearcomanda', name="crearcomanda"),
                       url(r'^productos$', 'gestiones.Mozo.views.seleccionarproductos', name="seleccionarproductos"),
                       url(r'^cargarproductos$', 'gestiones.Mozo.views.cargararproductosajax', name="cargarproductosajax"),
                       url(r'^cargarmesas$', 'gestiones.Mozo.views.cargararmesasjax', name="cargararmesasjax"),
                       url(r'^sacarmesas$', 'gestiones.Mozo.views.sacarmesasjax', name="sacarmesasjax"),
                       url(r'^guardarproducto$', 'gestiones.Mozo.views.guardarproductosajax', name="guardarproductosajax"),
                       url(r'^cargar$', 'gestiones.Mozo.views.cargarpanelajax', name="cargarpanelajax"),
                       url(r'^cancelarComanda$', 'gestiones.Mozo.views.cancelarComandajax', name="cancelarComandajax"),
                       url(r'^finalizar$', 'gestiones.Mozo.views.finalizar', name="finalizar"),
                       url(r'^volvermesas$', 'gestiones.Mozo.views.vistaMesas', name="vistaMesas"),
                       url(r'^guardarComanda$', 'gestiones.Mozo.views.guardarComanda', name="guardarComanda"),
)