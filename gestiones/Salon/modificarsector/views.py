from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import modificarSectorForm
from django.core.urlresolvers import reverse
from gestiones.Salon.altamesa.models import Sector


@permission_required('Administrador.is_admin', login_url="login")
def modificarsector(request, id_sector = None):


    sectores = Sector.objects.all().order_by('-activo')

    print(sectores)
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        sector = Sector.objects.get(pk=id_sector)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosSector = {'id': sector.id, 'descripcion': sector.descripcion, 'tipo': sector.tipo,
                     'activo': sector.activo}
    except:
        datosSector = ''
        sector=None

    #si se apreto el boton de modificar
    if request.method == 'POST' and sector != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarSectorForm(request.POST, instance=sector)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            descripcion = formulario.cleaned_data['descripcion']
            tipo = formulario.cleaned_data['tipo']
            activo = formulario.cleaned_data['activo']

            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            sector.descripcion = descripcion
            sector.tipo = tipo
            sector.activo = activo
            sector.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Salon/modificarsector/modificarsectorexito.html',
                                      {'formulario': formulario, 'sector': sectores},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Salon/modificarsector/modificarsector.html',
                                  {'formulario': formulario, 'sector': sectores},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarSectorForm(initial=datosSector)
        return render_to_response('Salon/modificarsector/modificarsector.html',
                                  {'formulario': formulario, 'sector': sectores},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarsectordel(request, id_sector):

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        sector = Sector.objects.get(pk=id_sector)
    except:
        sector=None

    #si se apreto el boton de modificar
    if request.method == 'GET' and sector != None:

        if sector.activo:
            sector.activo = False
        else:
            sector.activo = True

        sector.save()

    return HttpResponseRedirect(reverse('modificarsector'))