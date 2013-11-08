from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from gestiones.Producto.altaplato.forms import altaPlatoForm
from gestiones.Producto.producto.models import Plato



@permission_required('Administrador.is_admin', login_url="login")
def modificarplato(request, id_plato = None):

    #rescato los    usarios que son mozos
    platos = Plato.objects.all().order_by('nombre', 'seccion')

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        plato_id = Plato.objects.get(pk=id_plato)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosPlato = {'nombre': plato_id.nombre, 'precio': plato_id.precio,
                     'stock': plato_id.stock,
                     'enPromocion': plato_id.enPromocion, 'descuento': plato_id.descuento,
                     'seccion': plato_id.seccion}
    except:
        datosPlato = ''
        plato_id=None

    #si se apreto el boton de modificar
    if request.method == 'POST' and plato_id != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = altaPlatoForm(request.POST, instance=plato_id)

        #si el formulario es valido
        if formulario.is_valid():

            #rescato los datos de cada cmapo y los limpio
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            promocion = formulario.cleaned_data['enPromocion']
            descuento = formulario.cleaned_data['descuento']
            seccion = formulario.cleaned_data['seccion']
            if (seccion.categoria=='P'):
                #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
                plato_id.nombre = nombre
                plato_id.precio = precio
                plato_id.stock = stock
                plato_id.descripcion = descripcion
                plato_id.enPromocion = promocion
                plato_id.descuento = descuento
                plato_id.seccion = seccion
                plato_id.save()
                #mostramos que la operacion fue exitosa
                return render_to_response('Producto/modificarplato/modificarplatoexito.html',
                                          {'formulario': formulario, 'platos': platos},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('Producto/modificarplato/modificarplatoerror.html',
                                          {},
                                          context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/modificarplato/modificarplato.html',
                                  {'formulario': formulario, 'platos': platos},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = altaPlatoForm(initial=datosPlato)
        return render_to_response('Producto/modificarplato/modificarplato.html',
                                  {'formulario': formulario, 'platos': platos},
                                  context_instance=RequestContext(request))



@permission_required('Administrador.is_admin', login_url="login")
def modificarplatodel(request, id_plato):

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unPlato = Plato.objects.get(pk=id_plato)
    except:
        unPlato=None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unPlato != None:

        if unPlato.activo:
            unPlato.activo = False
        else:
            unPlato.activo = True

        unPlato.save()

    return HttpResponseRedirect(reverse('modificarplato'))
