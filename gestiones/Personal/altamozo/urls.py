from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'gestiones.Personal.altamozo.views.altamozo', name="altamozo"),

)



