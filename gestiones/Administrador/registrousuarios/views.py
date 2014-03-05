from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Administrador.models import permisosVistas
from gestiones.Administrador.registrousuarios.forms import registrousuariosForm


@permission_required('Administrador.is_admin', login_url="login")
def registrousuarios(request):

    if request.method == 'POST':

        formulario = registrousuariosForm(request.POST)

        print request.POST

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

            permisos = formulario.cleaned_data['permisos']

            #creamos el user mozo
            usuario = User.objects.create_user(usuario, email, contrasenia)

            #si el permiso es de admin
            if permisos.codename == 'is_admin':

                #rescato todos los permisos
                content_type = ContentType.objects.get_for_model(permisosVistas)
                permisosAll = Permission.objects.filter(content_type=content_type,codename__icontains = 'is_')

                #le asigno todos los permisos al user recien creado
                for p in permisosAll.all():
                    usuario.user_permissions.add(p)

                usuario.is_superuser = True
                usuario.is_staff = True

            else:
                #se los asigno al mozo recien creado
                usuario.user_permissions.add(permisos)

            #Actualizo y guardo al user
            usuario.first_name = nombre
            usuario.last_name = apellido

            usuario.tipoDoc = tipoDoc
            usuario.numeroDoc = numeroDoc
            usuario.telefono = telefono
            usuario.direccion = direccion
            usuario.turno = turno
            usuario.is_active = activo

            usuario.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/registrousuarios/registrousuariosexito.html', {},context_instance=RequestContext(request))

        return render_to_response('Administrador/registrousuarios/registrousuarios.html', {'formulario': formulario},
                                      context_instance=RequestContext(request))
    else:
        formulario = registrousuariosForm()
        return render_to_response('Administrador/registrousuarios/registrousuarios.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))
    #return render_to_response('Administrador/registrousuarios/registrousuarios.html', {}, context_instance=RequestContext(request))
