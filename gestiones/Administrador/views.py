from django.contrib.auth.decorators import permission_required
#from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Comanda.comanda.forms import altaEstrategiaComandaForm

#@login_required()
from gestiones.Comanda.comanda.models import EstrategiaComanda


@permission_required('Administrador.is_admin', login_url="logout")
def Administrador(request):
	return render_to_response('Administrador/administrador.html', {'user': request.user}, context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="logout")
def estrategias(request):
    if request.method == 'POST':
        formulario = altaEstrategiaComandaForm(request.POST)
        if formulario.is_valid():
            #capturamos y limpiamos los datos
            nombre = formulario.cleaned_data['nombre']
            horaI = formulario.cleaned_data['hora_inicio']
            horaf = formulario.cleaned_data['hora_fin']
            estC = EstrategiaComanda.objects.create(nombre=nombre, hora_inicio=horaI, hora_fin= horaf)
            return render_to_response('Administrador/altaEstCom.html', {}, context_instance=RequestContext(request))
        else:
            return render_to_response('Administrador/altaestrategiacomanda.html', {'formulario': formulario},context_instance=RequestContext(request))
    else:
        formulario=altaEstrategiaComandaForm()
        return render_to_response('Administrador/altaestrategiacomanda.html', {'formulario': formulario},context_instance=RequestContext(request))