from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Salon.altamesa.models import Sector
from gestiones.Salon.altasector.forms import altaSectorForm


@permission_required('Administrador.is_admin', login_url="login")
def altasector(request):
    if request.method == 'POST':

        formulario = altaSectorForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            tipo = formulario.cleaned_data['tipo']
            descripcion = formulario.cleaned_data['descripcion']
            activo = formulario.cleaned_data['activo']

            sector = Sector.objects.create(tipo=tipo, descripcion=descripcion, activo=activo)

            #mostramos que la operacion fue exitosa
            return render_to_response('Salon/altasector/altasectorexito.html', {},
                                      context_instance=RequestContext(request))

        return render_to_response('Salon/altasector/altasector.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:
        formulario = altaSectorForm()
        return render_to_response('Salon/altasector/altasector.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))
