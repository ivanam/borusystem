from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Salon.modificarmesa.views.modificarmesa', name="modificarmesa"),
                       url(r'^(?P<id_mesa>\d+)$', 'gestiones.Salon.modificarmesa.views.modificarmesa',
                           name="modificarmesa_id"),
                       url(r'^del/(?P<id_mesa>\d+)$', 'gestiones.Salon.modificarmesa.views.modificarmesadel',
                           name="modificarmesa_id_del"),


                       url(r'^buscar$', 'gestiones.Salon.modificarmesa.views.buscarmesasajax',
                           name="buscador_mesas_ajax"),

                       url(r'^buscarresultados$', 'gestiones.Salon.modificarmesa.views.buscarmesasajaxResultados',
                           name="buscador_mesas_ajax_resultados"),

                       url(r'^paginar', 'gestiones.Salon.modificarmesa.views.paginadorajaxResultados',
                           name="paginador_ajax_resultados_mesas"),


)

