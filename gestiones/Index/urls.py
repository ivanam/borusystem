from django.conf.urls import patterns, include, url
from .views import Index

urlpatterns = patterns('',
    
	url(r'^$', 'gestiones.Index.views.Index',name = "login"),
#url(r'^$',Index.as_view(),name = "login"),
#url(r'^$', login, {'template_name': 'Index/index.html', }, name="login"),
)