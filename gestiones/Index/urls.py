from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'gestiones.Index.views.Index',name = "login"),
)