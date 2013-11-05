from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Salon.modificarmesa.views.modificarmesa', name="modificarmesa"),
                       url(r'^(?P<id_mesa>\d+)$', 'gestiones.Salon.modificarmesa.views.modificarmesa',
                           name="modificarmesa_id"),
                       url(r'^del/(?P<id_mesa>\d+)$', 'gestiones.Salon.modificarmesa.views.modificarmesadel',
                           name="modificarmesa_id_del"),
)

