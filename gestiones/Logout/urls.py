from django.conf.urls import patterns, include, url
from .views import desloguearse

urlpatterns = patterns('',
 
url(r'^$', 'gestiones.Logout.views.desloguearse', name="logout"),

)