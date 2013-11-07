from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.altamenuejecutivo.views.altamenuejecutivo', name="altamenuejecutivo"),

)