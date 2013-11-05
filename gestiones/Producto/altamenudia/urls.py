from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Producto.altamenudia.views.altamenudia', name="altamenudia"),

)