from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from gestiones.Administrador.models import permisosVistas
from django.contrib.auth.models import Permission, User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import altaMozoForm


@permission_required('Administrador.is_admin', login_url="login")
def altamozo(request):
    if request.method == 'POST':
        formulario = altaMozoForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            usuario = formulario.cleaned_data['username']
            contrasenia = formulario.cleaned_data['password']
            nombre = formulario.cleaned_data['first_name']
            apellido = formulario.cleaned_data['last_name']
            email = formulario.cleaned_data['email']

            tipoDoc = formulario.cleaned_data['tipoDoc']
            numeroDoc = formulario.cleaned_data['numeroDoc']
            telefono = formulario.cleaned_data['telefono']
            direccion = formulario.cleaned_data['direccion']
            turno = formulario.cleaned_data['turno']
            activo = formulario.cleaned_data['is_active']

            #creamos el user mozo
            usuarioMozo = User.objects.create_user(usuario, email, contrasenia)
            #rescato los permiso de mozo
            content_type = ContentType.objects.get_for_model(permisosVistas)
            permisoMozo = Permission.objects.get(content_type=content_type, codename='is_mozo')
            #se los asigno al mozo recien creado
            usuarioMozo.user_permissions.add(permisoMozo)
            #Actualizo y guardo al user
            usuarioMozo.first_name = nombre
            usuarioMozo.last_name = apellido

            usuarioMozo.tipoDoc = tipoDoc
            usuarioMozo.numeroDoc = numeroDoc
            usuarioMozo.telefono = telefono
            usuarioMozo.direccion = direccion
            usuarioMozo.turno = turno
            usuarioMozo.is_active = activo

            usuarioMozo.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Personal/altamozo/altamozoexito.html', {}, context_instance=RequestContext(request))

        return render_to_response('Personal/altamozo/altamozo.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:
        formulario = altaMozoForm()
        return render_to_response('Personal/altamozo/altamozo.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))