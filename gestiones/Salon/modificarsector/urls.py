from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Salon.modificarsector.views.modificarsector', name="modificarsector"),
                       url(r'^(?P<id_sector>\d+)$', 'gestiones.Salon.modificarsector.views.modificarsector',
                           name="modificarsector_id"),
                       url(r'^del/(?P<id_sector>\d+)$', 'gestiones.Salon.modificarsector.views.modificarsectordel',
                           name="modificarsector_id_del"),
)