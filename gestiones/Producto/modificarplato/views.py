# -*- encoding: utf-8 -*-  
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from boru.settings import PAGINADO_PRODUCTOS
from gestiones.Producto.modificarplato.forms import modificarPlato
from gestiones.Producto.producto.models import Plato


@permission_required('Administrador.is_admin', login_url="login")
def modificarplato(request, id_plato=None):
    #rescato todos los platos

    platos_lista = Plato.objects.all().order_by('nombre')
    paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)
    platos = paginator.page(1)

    try:
        #obtengo en el caso de que venga el id por GET, al pl
        # ato
        plato_id = Plato.objects.get(pk=id_plato)

        #creo diccionario con los datos del plato para mostrarlos ne el formulario
        datosPlato = {'nombre': plato_id.nombre, 'precio': plato_id.precio,
                      'stock': plato_id.stock, 'descripcion': plato_id.descripcion,
                      'enPromocion': plato_id.enPromocion, 'descuento': plato_id.descuento,
                      'seccion': plato_id.seccion, 'activo': plato_id.activo}

    except:
        datosPlato = ''
        plato_id = None

    #si se apreto el boton de modificar
    if request.method == 'POST' and plato_id != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarPlato(request.POST, instance=plato_id)

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
            activo = formulario.cleaned_data['activo']

            plato_id.nombre = nombre
            plato_id.precio = precio
            plato_id.stock = stock
            plato_id.descripcion = descripcion
            plato_id.enPromocion = promocion
            plato_id.descuento = descuento
            plato_id.seccion = seccion
            plato_id.activo = activo
            plato_id.save()

            #si el plato no tiene stock o se desactivo
            if stock == 0 or activo == False:
                #rescato los menues del dia en los que esta el plato
                menuDia = plato_id.estoyEnMenuDia()
                #los recorro para desactivarlos
                for md in menuDia:
                    md.activo = False
                    md.save()

                #lo mismo para los menues ejecutivos
                menuEje = plato_id.estoyEnMenuEjecutivo()
                #los recorro para desactivarlos
                for me in menuEje:
                    me.activo = False
                    me.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/modificarplato/modificarplatoexito.html',
                                      {'formulario': formulario, 'platos': platos},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/modificarplato/modificarplato.html',
                                  {'formulario': formulario, 'platos': platos},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarPlato(initial=datosPlato)
        return render_to_response('Producto/modificarplato/modificarplato.html',
                                  {'formulario': formulario, 'platos': platos},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarplatodel(request, id_plato):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unPlato = Plato.objects.get(pk=id_plato)
    except:
        unPlato = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unPlato != None:
        unPlato.cambiarEstado()
        unPlato.save()

    return HttpResponseRedirect(reverse('modificarplato'))



@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by('nombre')[:30]

        return render_to_response('Producto/modificarplato/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            platos = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre')
        else:
            platos_lista = Plato.objects.all().order_by("nombre")
            paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)
            platos = paginator.page(1)

        return render_to_response('Producto/modificarplato/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))





@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        platos_lista = Plato.objects.all().order_by('nombre')
        paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)

        try:
            platos = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            platos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            platos = paginator.page(paginator.num_pages)

        return render_to_response('Producto/modificarplato/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))





