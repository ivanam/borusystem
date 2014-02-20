from django.conf.urls import patterns, url

urlpatterns = patterns('',

            url(r'^(?P<pagina>\d+)*$', 'gestiones.Carta.modificarseccion.views.modificarseccion',
                name="modificarseccion"),
            url(r'^seccion/(?P<id_seccion>\d+)$', 'gestiones.Carta.modificarseccion.views.modificarseccion',
                           name="modificarseccion_id"),
            url(r'^del/(?P<id_seccion>\d+)$', 'gestiones.Carta.modificarseccion.views.modificarsecciondel',
                name="modificarseccion_id_del"),

)