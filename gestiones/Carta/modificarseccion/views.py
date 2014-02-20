from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from boru.settings import PAGINADO_SECCIONES
from gestiones.Carta.modificarseccion.forms import modificarSeccionForm
from gestiones.Carta.altacarta.models import Carta, SeccionCarta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


@permission_required('Administrador.is_admin', login_url="login")
def modificarseccion (request, id_seccion=None,pagina=1):

    if pagina == None:
        pagina = 1

    #rescato las secciones
    #secciones = SeccionCarta.objects.all().order_by('-activo')
    secciones_lista = SeccionCarta.objects.all().order_by('nombre')
    paginator = Paginator(secciones_lista, PAGINADO_SECCIONES)
    secciones = paginator.page(pagina)

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaSeccion = SeccionCarta.objects.get(pk=id_seccion)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosSeccion = {'id': unaSeccion.id, 'nombre': unaSeccion.nombre, 'categoria': unaSeccion.categoria, 'imagen': unaSeccion.imagen}

    except:
        datosSeccion = ''
        unaSeccion = None


        #si se apreto el boton de modificar
    if request.method == 'POST' and unaSeccion != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarSeccionForm(request.POST, instance=unaSeccion)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            nombre = formulario.cleaned_data['nombre']
            #categoria = formulario.cleaned_data['categoria']
            imagen = formulario.cleaned_data['imagen']



            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            unaSeccion.nombre = nombre
            #unaSeccion.categoria = categoria
            unaSeccion.imagen = imagen
            unaSeccion.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Carta/modificarseccionExito.html',
                                      {'formulario': formulario, 'secciones': secciones},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresado
        return render_to_response('Carta/modificarseccion.html',
                                  {'formulario': formulario, 'secciones': secciones},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarSeccionForm(initial=datosSeccion)
        return render_to_response('Carta/modificarseccion.html',
                                  {'formulario': formulario, 'secciones': secciones},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarsecciondel(request, id_seccion):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaSeccion = SeccionCarta.objects.get(pk=id_seccion)
    except:
        unaSeccion = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unaSeccion != None:

        if unaSeccion.activo:
            unaSeccion.activo = False
        else:
            unaSeccion.activo = True

        unaSeccion.save()

    return HttpResponseRedirect(reverse('modificarseccion'))