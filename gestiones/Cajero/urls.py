from django.conf.urls import patterns, include, url
from .views import Cajero
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    
    url(r'^$', 'gestiones.Cajero.views.Cajero', name="cajero"),
    url(r'^detalle$', 'gestiones.Cajero.views.detalle_comanda_ajax', name="detalle_comanda_ajax"),

)