from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from gestiones.Administrador.models import permisosVistas
from django.contrib.auth.models import Permission, User
from django.http import HttpResponseRedirect
from .forms import altaMesaForm
#from altasector.models import Sector
from gestiones.Salon.altamesa.models import Mesa


@permission_required('Administrador.is_admin', login_url="login")
def altamesa(request):
    if request.method == 'POST':
        formulario = altaMesaForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            tipo = formulario.cleaned_data['tipo']
            capacidad = formulario.cleaned_data['capacidad']
            ocupada = formulario.cleaned_data['ocupada']
            activo = formulario.cleaned_data['activo']
            sector = formulario.cleaned_data['sector']

            #creamos la mesa
            mesa = Mesa()
            #rescato los permiso de mozo
            #content_type = ContentType.objects.get_for_model(permisosVistas)
            #permisoMozo = Permission.objects.get(content_type=content_type, codename='is_mozo')
            #se los asigno al mozo recien creado
            #usuarioMozo.user_permissions.add(permisoMozo)
            #Actualizo y guardo al user
            mesa.tipo = tipo
            mesa.capacidad = capacidad
            mesa.ocupada = ocupada
            mesa.activo = activo
            mesa.sector = sector

            mesa.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Salon/altamesa/altamesaexito.html', {}, context_instance=RequestContext(request))

        return render_to_response('Salon/altamesa/altamesa.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:
        formulario = altaMesaForm()
        return render_to_response('Salon/altamesa/altamesa.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="logout")
def altamesaexito(request):
    return render_to_response('Salon/altamesa/altamesaexito.html', context_instance=RequestContext(request))