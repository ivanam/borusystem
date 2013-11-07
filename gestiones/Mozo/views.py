from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    return render_to_response('Mozo/mozo2.html', {}, context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def crearcomanda (request):
    print ("creamos la comanda")
    panel_seleccionar_mesa=render_to_response('Mozo/panel_mesas_seleccionadas.html', {}, context_instance=RequestContext(request))
    return render_to_response('Mozo/seleccionar_mesas.html', {'panel_seleccionar_mesa':panel_seleccionar_mesa}, context_instance=RequestContext(request))
    #return HttpResponseRedirect('seleccionarmesas')

