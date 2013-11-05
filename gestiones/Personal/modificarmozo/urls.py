from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'gestiones.Personal.modificarmozo.views.modificarmozo', name="modificarmozo"),
    url(r'^(?P<id_user>\d+)$', 'gestiones.Personal.modificarmozo.views.modificarmozo',
       name="modificarmozo_id"),
    url(r'^del/(?P<id_user>\d+)$', 'gestiones.Personal.modificarmozo.views.modificarmozodel',
       name="modificarmozo_id_del"),
)