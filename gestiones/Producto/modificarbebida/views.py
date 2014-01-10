from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from boru.settings import PAGINADO_PRODUCTOS
from .forms import modificarBebida
from django.core.urlresolvers import reverse
from gestiones.Producto.producto.models import Bebida


@permission_required('Administrador.is_admin', login_url="login")
def modificarbebida(request, id_bebida = None):
    #rescato las bebidas
    bebidas_lista = Bebida.objects.all().order_by('nombre')
    paginator = Paginator(bebidas_lista, PAGINADO_PRODUCTOS)
    bebidas = paginator.page(1)

    try:
        #obtengo en el caso de que venga el id por GET, a la bebida
        unaBebida = Bebida.objects.get(pk=id_bebida)

        #creo diccionario con los datos de la bebida para mostrarlos en el formulario
        datosBebida = {'id': unaBebida.id, 'nombre': unaBebida.nombre, 'precio': unaBebida.precio,
                       'stock': unaBebida.stock, 'activo': unaBebida.activo, 'marca': unaBebida.marca,
                       'enPromocion': unaBebida.enPromocion, 'descuento': unaBebida.descuento,
                       'seccion': unaBebida.seccion}

    except:
        datosBebida = ''
        unaBebida = None

    #si se apreto el boton de modificar
    if request.method == 'POST' and unaBebida != None:

        #le indico al form que tome los datos del request y le paso la instancia de bebida que obtuve mas arriba
        formulario = modificarBebida(request.POST, instance=unaBebida)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada campo y los limpio
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            activo = formulario.cleaned_data['activo']
            marca = formulario.cleaned_data['marca']
            enPromocion = formulario.cleaned_data['enPromocion']
            descuento = formulario.cleaned_data['descuento']
            seccion = formulario.cleaned_data['seccion']

            #seteo los nuevos datos en el objeto unaBebida que obtuvimos al principio
            unaBebida.nombre = nombre
            unaBebida.precio = precio
            unaBebida.stock = stock
            unaBebida.activo = activo
            unaBebida.marca = marca
            unaBebida.enPromocion = enPromocion
            unaBebida.descuento = descuento
            unaBebida.seccion = seccion
            unaBebida.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/modificarbebida/modificarbebidaexito.html',
                                      {'formulario': formulario, 'bebidas': bebidas},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/modificarbebida/modificarbebida.html',
                                  {'formulario': formulario, 'bebidas': bebidas},
                                  context_instance=RequestContext(request))

    else:
        #si no apretamos el boton modificar bebida y seleccionamos alguna bebida mostramos sus datos, sino mostramos el form vacio
        formulario = modificarBebida(initial=datosBebida)
        return render_to_response('Producto/modificarbebida/modificarbebida.html',
                                  {'formulario': formulario, 'bebidas': bebidas},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarbebidadel(request, id_bebida):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaBebida = Bebida.objects.get(pk=id_bebida)
    except:
        unaBebida = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unaBebida != None:

        unaBebida.cambiarEstado()
        unaBebida.save()

    return HttpResponseRedirect(reverse('modificarbebida'))



@permission_required('Administrador.is_admin', login_url="login")
def buscarbebidasajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = Bebida.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) | Q(marca__icontains=q)).order_by('nombre')[:30]

        return render_to_response('Producto/modificarbebida/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarbebidasajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            bebidas = Bebida.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) | Q(marca__icontains=q) ).order_by('nombre')
        else:
            bebidas_lista = Bebida.objects.all().order_by("nombre")
            paginator = Paginator(bebidas_lista, PAGINADO_PRODUCTOS)
            bebidas = paginator.page(1)

        return render_to_response('Producto/modificarbebida/busquedaresultados_items.html', {'bebidas': bebidas},
                                  context_instance=RequestContext(request))



@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        bebidas_lista = Bebida.objects.all().order_by('nombre')
        paginator = Paginator(bebidas_lista, PAGINADO_PRODUCTOS)

        try:
            bebidas = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            bebidas = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            bebidas = paginator.page(paginator.num_pages)

        return render_to_response('Producto/modificarbebida/busquedaresultados_items.html', {'bebidas': bebidas},
                                  context_instance=RequestContext(request))

