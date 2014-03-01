from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'gestiones.Administrador.registrousuarios.views.registrousuarios', name="registrousuarios"),
)
