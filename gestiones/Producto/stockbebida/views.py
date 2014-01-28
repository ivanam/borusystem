from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from boru.settings import PAGINADO_PRODUCTOS
from gestiones.Producto.stockbebida.forms import stockBebida
from gestiones.Producto.producto.models import Bebida

@permission_required('Administrador.is_admin', login_url="login")
def stockbebida(request, id_plato=None):
    #rescato todos los bebida
    platos_lista = Bebida.objects.all().order_by('nombre')
    paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)
    platos = paginator.page(1)

    error = ''
    stock_valido = True

    try:
        #obtengo en el caso de que venga el id por GET, al plato
        plato_id = Bebida.objects.get(pk=id_plato)

        #creo diccionario con los datos del plato para mostrarlos ne el formulario
        datosPlato =  {'nombre': plato_id.nombre, 'precio': plato_id.precio,
                      'stock': plato_id.stock}

    except:
        datosPlato = ''
        plato_id = None

    #si se apreto el boton de modificar
    if request.method == 'POST' and plato_id != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = stockBebida(request.POST, instance=plato_id)

        try:
            #rescato el valor que queiro agregar al stock y tato de converirlo en entero
            addProducto = int(request.POST.get('addProducto'))
        except:
            #si lo que ingresaron no fue un entero indico el error
            error = 'El stock ingresado debe ser un numero entero.'
            stock_valido = False

        #si el formulario es valido
        if formulario.is_valid() and stock_valido:

            #calculo nuevo stock
            stockNuevo = plato_id.stock+addProducto

            #si el nuevo stock es menor o igual a 0
            if stockNuevo <= 0:

                #si es menor a 0 lo pongo en 0
                plato_id.stock = 0
                plato_id.save()
            else:
                plato_id.stock = stockNuevo
                plato_id.save()


            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/stockbebida/stockbebidaexito.html',
                                      {'formulario': formulario, 'platos': platos, 'datosPlato': datosPlato},
                                      context_instance=RequestContext(request))



        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/stockbebida/stockbebida.html',
                                  {'formulario': formulario, 'platos': platos,'datosPlato': datosPlato,'error':error},
                                  context_instance=RequestContext(request))


    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = stockBebida(initial=datosPlato)
        return render_to_response('Producto/stockbebida/stockbebida.html',
                                  {'formulario': formulario, 'platos': platos, 'datosPlato': datosPlato,'error':error},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_admin', login_url="login")
def modificarbebidadel(request, id_plato):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unPlato = Bebida.objects.get(pk=id_plato)
    except:
        unPlato = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unPlato != None:
        unPlato.cambiarEstado()
        unPlato.save()

    return HttpResponseRedirect(reverse('stockbebida'))



@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = Bebida.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by('nombre')[:30]

        return render_to_response('Producto/stockbebida/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            platos = Bebida.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre')
        else:
            platos_lista = Bebida.objects.all().order_by("nombre")
            paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)
            platos = paginator.page(1)

        return render_to_response('Producto/stockbebida/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))





@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        platos_lista = Bebida.objects.all().order_by('nombre')
        paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)

        try:
            platos = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            platos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            platos = paginator.page(paginator.num_pages)

        return render_to_response('Producto/stockbebida/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))





