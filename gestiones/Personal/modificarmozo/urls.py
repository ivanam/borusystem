from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'gestiones.Personal.modificarmozo.views.modificarmozo', name="modificarmozo"),
    url(r'^(?P<id_user>\d+)$', 'gestiones.Personal.modificarmozo.views.modificarmozo',
       name="modificarmozo_id"),
    url(r'^del/(?P<id_user>\d+)$', 'gestiones.Personal.modificarmozo.views.modificarmozodel',
       name="modificarmozo_id_del"),

    url(r'^buscar$', 'gestiones.Personal.modificarmozo.views.buscarmozosajax',
        name="buscador_mozos_ajax"),
    url(r'^buscarresultados$', 'gestiones.Personal.modificarmozo.views.buscarmozosajaxResultados',
        name="buscador_mozos_ajax_resultados"),
    url(r'^paginar', 'gestiones.Personal.modificarmozo.views.paginadorajaxResultados',
        name="paginador_ajax_resultados_mozos"),
)