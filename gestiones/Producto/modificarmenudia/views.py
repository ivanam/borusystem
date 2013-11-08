from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Producto.modificarmenudia.forms import modificarMenuDiaForm
from gestiones.Producto.producto.models import DelDia, Plato
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


@permission_required('Administrador.is_admin', login_url="login")
def modificarmenudia(request, id_menu = None):

    #rescato los menues
    menues = DelDia.objects.all().order_by('-activo')

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unMenu = DelDia.objects.get(pk=id_menu)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosMenu = {'id': unMenu.id, 'nombre': unMenu.nombre, 'precio': unMenu.precio, 'stock':unMenu.stock, 'descripcion': unMenu.descripcion,
                     'fecha_Inicio': unMenu.fecha_Inicio, 'platos': unMenu.platos}

    except:
        datosMenu = ''
        unMenu=None


     #si se apreto el boton de modificar
    if request.method == 'POST' and unMenu != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarmenudia(request.POST, instance=unMenu)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha_Inicio = formulario.cleaned_data['fecha_Inicio']
            platos = formulario.cleaned_data['platos']


            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            unMenu.nombre = nombre
            unMenu.precio = precio
            unMenu.stock = stock
            unMenu.descripcion= descripcion
            unMenu.fecha_Inicio= fecha_Inicio
            unMenu.platos = platos
            unMenu.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/modificarmenudia/modificarmenudiaExito.html',
                                      {'formulario': formulario, 'menues': menues},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/modificarmenudia/modificarmenudia.html',
                                  {'formulario': formulario, 'menues': menues},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarMenuDiaForm(initial=datosMenu)
        return render_to_response('Producto/modificarmenudia/modificarmenudia.html',
                                  {'formulario': formulario, 'menues': menues},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarmenudel(request, id_menu):

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unMenu = DelDia.objects.get(pk=id_menu)
    except:
        unaMenu=None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unMenu != None:

        if unMenu.activo:
            unMenu.activo = False
        else:
            unMenu.activo = True

        unMenu.save()

    return HttpResponseRedirect(reverse('modificarmenudia'))