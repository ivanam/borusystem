from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'gestiones.Administrador.modificarusuarios.views.modificarusuarios', name="modificarusuarios"),
)