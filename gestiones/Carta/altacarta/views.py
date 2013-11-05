from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Carta.altacarta.forms import altaCartaForm
from gestiones.Carta.altacarta.models import Carta
import datetime
from datetime import date

@permission_required('Administrador.is_admin', login_url="login")
def altacarta(request):
    if request.method == 'POST':
        formulario = altaCartaForm(request.POST)
        if formulario.is_valid():
            #capturamos y limpiamos los datos
            nombre = formulario.cleaned_data['nombre']
            vigente = formulario.cleaned_data['vigente']
            if vigente:
                try:
                    cartas = Carta.objects.get(vigente=True)
                    cartas.vigente=False
                    cartas.save()
                except Exception:
                    print ("Primera Carta Creada")
            fecha = datetime.date.today()
            carta = Carta.objects.create(nombre=nombre, vigente=vigente, fecha=fecha)
            return render_to_response('Carta/altacartaexito.html', {}, context_instance=RequestContext(request))
        else:
            return render_to_response('Carta/altacarta.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))
    else:
        formulario=altaCartaForm()
        return render_to_response('Carta/altacarta.html', {'formulario': formulario},context_instance=RequestContext(request))
