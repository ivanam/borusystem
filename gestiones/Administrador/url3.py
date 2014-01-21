from django.conf.urls import patterns, include, url
from .views import Administrador
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

url(r'^$', 'gestiones.Administrador.views.AltaCajero', name="altaCajero"),

)
