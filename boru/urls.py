from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.admin import site

#site.register(Permission)
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boru.views.home', name='home'),
    # url(r'^boru/', include('boru.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
    
    #URLS propias del Proyecto Boru
    url(r'^', include('gestiones.Index.urls')),


    url(r'^mozo/', include('gestiones.Mozo.urls')),
    url(r'^cajero/', include('gestiones.Cajero.urls')),

    url(r'^administrador/', include('gestiones.Administrador.urls')),
    #url(r'^administrador/listarImprimir/', include('gestiones.Administrador.urls')),


    url(r'^administrador/altaAdministrador/', include('gestiones.Administrador.url2')),
    url(r'^administrador/altaCajero/', include('gestiones.Administrador.url3')),
    url(r'^administrador/modificarUsuarios/', include('gestiones.Administrador.url_modificarUsuario')),
    url(r'^administrador/altabebida/', include('gestiones.Producto.altabebida.urls')),
    url(r'^administrador/modificarbebida/', include('gestiones.Producto.modificarbebida.urls')),
    url(r'^administrador/stockbebida/', include('gestiones.Producto.stockbebida.urls')),
    url(r'^administrador/stockplato/', include('gestiones.Producto.stockplato.urls')),
    url(r'^administrador/altamenudia/', include('gestiones.Producto.altamenudia.urls')),
    url(r'^administrador/altamenuejecutivo/', include('gestiones.Producto.altamenuejecutivo.urls')),
    url(r'^administrador/modificarmenudia/', include('gestiones.Producto.modificarmenudia.urls')),
    url(r'^administrador/modificarmenuejecutivo/', include('gestiones.Producto.modificarmenuejecutivo.urls')),
    url(r'^administrador/altaplato/', include('gestiones.Producto.altaplato.urls')),
    url(r'^administrador/modificarplato/', include('gestiones.Producto.modificarplato.urls')),

    url(r'^administrador/altamozo/', include('gestiones.Personal.altamozo.urls')),
    url(r'^administrador/modificarmozo/', include('gestiones.Personal.modificarmozo.urls')),
    url(r'^administrador/eliminarmozo/', include('gestiones.Personal.eliminarmozo.urls')),

    url(r'^administrador/altamesa/', include('gestiones.Salon.altamesa.urls')),
    url(r'^administrador/modificarmesa/', include('gestiones.Salon.modificarmesa.urls')),
    url(r'^administrador/altasector/', include('gestiones.Salon.altasector.urls')),
    url(r'^administrador/modificarsector/', include('gestiones.Salon.modificarsector.urls')),

    url(r'administrador/altacarta', include('gestiones.Carta.altacarta.urls')),
    url(r'administrador/altaseccion', include('gestiones.Carta.altaseccion.urls')),
    url(r'administrador/modificarseccion', include('gestiones.Carta.modificarseccion.urls')),
    url(r'logout', include('gestiones.Logout.urls')),

)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)