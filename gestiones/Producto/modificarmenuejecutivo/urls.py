from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

            url(r'^$', 'gestiones.Producto.modificarmenuejecutivo.views.modificarmenuejecutivo',
                name="modificarmenuejecutivo"),
            url(r'^(?P<id_menue>\d+)$', 'gestiones.Producto.modificarmenuejecutivo.views.modificarmenuejecutivo',
                           name="modificarmenue_id"),
            url(r'^del/(?P<id_menue>\d+)$', 'gestiones.Producto.modificarmenuejecutivo.views.modificarmenuedel',
                name="modificarmenue_id_del"),

)