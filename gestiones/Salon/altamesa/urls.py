from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Salon.altamesa.views.altamesa', name="altamesa"),
                       url(r'^altamesaexito$', 'gestiones.Salon.altamesa.views.altamesaexito', name="altamesaexito"),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)