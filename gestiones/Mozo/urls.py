from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Mozo.views.inicio', name="mozo"),
                       url(r'^comanda$', 'gestiones.Mozo.views.crearcomanda', name="crearcomanda"),
)