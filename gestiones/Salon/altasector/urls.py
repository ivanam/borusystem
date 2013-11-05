from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Salon.altasector.views.altasector', name="altasector"),

)
