from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Carta.altaseccion.forms import altaSeccionForm
from gestiones.Carta.altacarta.models import Carta, SeccionCarta

@permission_required('Administrador.is_admin', login_url="login")
def altaseccion(request):
    if request.method == 'POST':
        formulario=altaSeccionForm(request.POST)
        if formulario.is_valid():
            try:
                carta = Carta.objects.get(vigente=True)
                nombre = formulario.cleaned_data['nombre']
                categoria = formulario.cleaned_data['categoria']
                seccion = SeccionCarta.objects.create(nombre=nombre, categoria=categoria, activo=True, cartavigente=carta)
                carta.secciones.add(seccion)
                carta.save()
                return render_to_response('Carta/altaseccionExito.html', {},context_instance=RequestContext(request))
            except Exception:
                return render_to_response('Carta/altaseccionError.html', {},context_instance=RequestContext(request))
        else:
            return render_to_response('Carta/altaseccion.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))
    else:
        formulario=altaSeccionForm()
        return render_to_response('Carta/altaseccion.html', {'formulario': formulario},context_instance=RequestContext(request))
