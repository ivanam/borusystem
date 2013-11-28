from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',

            url(r'^$', 'gestiones.Carta.modificarseccion.views.modificarseccion',
                name="modificarseccion"),
            url(r'^(?P<id_seccion>\d+)$', 'gestiones.Carta.modificarseccion.views.modificarseccion',
                           name="modificarseccion_id"),
            url(r'^del/(?P<id_seccion>\d+)$', 'gestiones.Carta.modificarseccion.views.modificarsecciondel',
                name="modificarseccion_id_del"),

)