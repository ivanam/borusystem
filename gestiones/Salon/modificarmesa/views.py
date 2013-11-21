from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import modificarMesa
from django.core.urlresolvers import reverse
from gestiones.Salon.altamesa.models import Mesa


@permission_required('Administrador.is_admin', login_url="login")
def modificarmesa(request, id_mesa=None):
    #rescato los    usarios que son mozos
    mesas = Mesa.objects.all().order_by('-activo')

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaMesa = Mesa.objects.get(pk=id_mesa)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosMesa = {'id': unaMesa.id, 'tipo': unaMesa.tipo, 'capacidad': unaMesa.capacidad,
                     'ocupada': unaMesa.ocupada, 'activo': unaMesa.activo, 'sector': unaMesa.sector}

    except:
        datosMesa = ''
        unaMesa = None

    #si se apreto el boton de modificar
    if request.method == 'POST' and unaMesa != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarMesa(request.POST, instance=unaMesa)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            tipo = formulario.cleaned_data['tipo']
            capacidad = formulario.cleaned_data['capacidad']
            ocupada = formulario.cleaned_data['ocupada']
            activo = formulario.cleaned_data['activo']
            sector = formulario.cleaned_data['sector']

            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            unaMesa.tipo = tipo
            unaMesa.capacidad = capacidad
            unaMesa.ocupada = ocupada
            unaMesa.activo = activo
            unaMesa.sector = sector
            unaMesa.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Salon/modificarmesa/modificarmesaexito.html',
                                      {'formulario': formulario, 'mesas': mesas},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Salon/modificarmesa/modificarmesa.html',
                                  {'formulario': formulario, 'mesas': mesas},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarMesa(initial=datosMesa)
        return render_to_response('Salon/modificarmesa/modificarmesa.html',
                                  {'formulario': formulario, 'mesas': mesas},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarmesadel(request, id_mesa):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaMesa = Mesa.objects.get(pk=id_mesa)
    except:
        unaMesa = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unaMesa != None:

        unaMesa.cambiarEstado()
        unaMesa.save()

    return HttpResponseRedirect(reverse('modificarmesa'))