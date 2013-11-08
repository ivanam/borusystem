from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from gestiones.Salon.altamesa.models import Mesa


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    return render_to_response('Mozo/mozo.html', {}, context_instance=RequestContext(request))



@permission_required('Administrador.is_mozo', login_url="login")
def crearcomanda(request):

    #si se envio el formulario
    if request.method == 'POST':
        print("post")
        #si lo enviado es un entero
        #if isinstance(request.POST['cantidadC'], int):
        print("valid")
        #lo guardo ne una variable de session
        request.session['cantidadC']=request.POST['cantidadC']
        #recupero las mesas que estan activas
        mesas=Mesa.objects.filter(activo__exact=1)
        #recupero el panel que muestra las mesas seleccionadas
        panel_seleccionar_mesa=get_template('Mozo/panel_mesas_seleccionadas.html')
        #lo inserto en el resto del template y lo muestro
        return render_to_response('Mozo/seleccionar_mesas.html', {'panel_seleccionar_mesa':panel_seleccionar_mesa.render( Context({}) ),'mesas':mesas }, context_instance=RequestContext(request))

        #return HttpResponseRedirect(reverse('mozo'))
    else:
        print("else")
        #si trato de entrar sin haber enviado el form,me vuelve a la primera pagina
        return HttpResponseRedirect(reverse('mozo'))