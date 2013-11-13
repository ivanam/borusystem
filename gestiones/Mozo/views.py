from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Salon.altamesa.models import Mesa


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    return render_to_response('Mozo/mozo.html', {}, context_instance=RequestContext(request))



@permission_required('Administrador.is_mozo', login_url="login")
def crearcomanda(request):

    #si se envio el formulario
    if request.method == 'POST':

        cantidad=request.POST['cantidadC']

        #si lo enviado es un entero
        if cantidad.isdigit():

            #lo guardo ne una variable de session
            request.session['cantidadC']=cantidad
            #recupero las mesas que estan activas
            mesas=Mesa.objects.filter(activo__exact=1)
            #recupero el panel que muestra las mesas seleccionadas
            panel_seleccionar_mesa=get_template('Mozo/panel_mesas_seleccionadas.html')
            #lo inserto en el resto del template y lo muestro
            return render_to_response('Mozo/seleccionar_mesas.html', {'panel_seleccionar_mesa':panel_seleccionar_mesa.render( Context({'cantidadC': cantidad}) ),'mesas':mesas }, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect(reverse('mozo'))

    else:
        #si trato de entrar sin haber enviado el form,me vuelve a la primera pagina
        return HttpResponseRedirect(reverse('mozo'))

def seleccionarproductos(request):
    seccion = SeccionCarta.objects.filter(activo__exact=1)
    panel_seleccionar_producto=get_template('Mozo/panel_menu_seleccionado.html')
    return render_to_response('Mozo/seleccionar_menu.html', {'seccion': seccion, 'panel_seleccionar_mesa':panel_seleccionar_producto.render( Context({}) )}, context_instance=RequestContext(request))

def cargararproductosajax(request):
    print("Entre en la funcion de vista")
    if request.method == 'GET':
        id_seccion = request.GET['id_seccion']
        seccion = SeccionCarta.objects.get(pk=id_seccion)
        return render_to_response('Mozo/productos_items.html', {'seccion': seccion}, context_instance=RequestContext(request))

