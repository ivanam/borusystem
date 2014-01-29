# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from boru.settings import PAGINADO_PRODUCTOS_MENUES
from gestiones.Producto.modificarmenuejecutivo.forms import modificarMenuEjecutivoForm
from gestiones.Producto.producto.models import Ejecutivo, Plato
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse


@permission_required('Administrador.is_admin', login_url="login")
def modificarmenuejecutivo(request, id_menu=None):

    #rescato los platos
    platos_lista = Plato.objects.all().order_by('nombre')
    paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS_MENUES)
    platos = paginator.page(1)

    #rescato los menues
    menues = Ejecutivo.objects.all().order_by('nombre')

    try:
        #obtengo en el caso de que venga el id por GET, al menu
        unMenu = Ejecutivo.objects.get(pk=id_menu)

        #creo diccionario con los datos del menu para mostrarlos ne el formulario
        datosMenu = {'id': unMenu.id, 'nombre': unMenu.nombre, 'precio': unMenu.precio, 'stock': unMenu.stock,
                     'descripcion': unMenu.descripcion,'fecha_Inicio': unMenu.fecha_Inicio , 'fecha_fin': unMenu.fecha_fin
                    ,'seccion': unMenu.seccion, 'activo': unMenu.activo, 'platos': unMenu.platos}
    except:
        datosMenu = ''
        unMenu = None



    #compruebo si existe sesion y si hay seleccionado algun menu
    platos_selec = get_template('Producto/modificarmenuejecutivo/menuejecutivo_platos.html')
    platos_selec_sesion = get_template('Producto/modificarmenuejecutivo/menuejecutivo_platos_ajax.html')
    listaPlatos = []
    listaPlatos_sesion = []

    try:

        #platos originales
        for p in unMenu.platos.all():
            listaPlatos.append(Plato.objects.get(pk=p.id))

        try:
            lista = request.session['listaProductosModificarMenuEjecutivo']
            #platos que selecciones si hay
            for s in lista:
                listaPlatos_sesion.append(Plato.objects.get(pk=s))
        except:
            pass

        platosLista = listaPlatos
        platosLista_sesion = listaPlatos_sesion

    except:
        platosLista = []
        platosLista_sesion = []



    #si se apreto el boton de modificar
    if request.method == 'POST' and unMenu != None:

        #le indico al form que tome los datos del request y le paso la instancia del menu  que obtuve mas arriba
        formulario = modificarMenuEjecutivoForm(request.POST, instance=unMenu)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha_Inicio = formulario.cleaned_data['fecha_Inicio']
            fecha_fin = formulario.cleaned_data['fecha_fin']
            seccion = formulario.cleaned_data['seccion']
            activo = formulario.cleaned_data['activo']

            #recupero las ids de los platos que quiero agregar al menu
            lista_platos_seleccionado = request.POST.getlist('platos')
            #para guardar la lista de platos
            prod = []

            #seteo los nuevos datos en el objeto unMenu que obtuvimos al principio
            unMenu.nombre = nombre
            unMenu.precio = precio
            unMenu.stock = stock
            unMenu.descripcion = descripcion
            unMenu.fecha_Inicio = fecha_Inicio
            unMenu.fecha_fin = fecha_fin
            unMenu.seccion = seccion

            #miro los platos para asegurarme que todos estan en regla(con stock y activos)
            for p in lista_platos_seleccionado:
                aux = Plato.objects.get(pk=p)

                if aux.stock == 0 or aux.activo == False:
                    activo=False

                prod.append(aux)

            #seteo el estado del menu
            unMenu.activo = activo
            unMenu.save()

            #limpio la lista de platos
            unMenu.limpiar_platos()
            #las recorro y rescato los platos y los asigno al menu
            for p in prod:
                unMenu.agregar_plato(p)

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/modificarmenuejecutivo/modificarmenuejecutivoExito.html',
                                      {'formulario': formulario, 'menues': menues},
                                      context_instance=RequestContext(request))


        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/modificarmenuejecutivo/modificarmenuejecutivo.html',
                                  {'id_menu':id_menu,'formulario': formulario, 'menues': menues, 'plato': platos,
                                   'lista_platos': platos_selec.render(Context({'platos': platosLista})),
                                   'lista_platos_sesion': platos_selec_sesion.render(
                                       Context({'platos': platosLista_sesion}))
                                  }, context_instance=RequestContext(request))


    else:
        #si no apretamos el boton modificar menu y seleccionamos algun menu, mostramos sus datos, sino mostramos el form vacio
        formulario = modificarMenuEjecutivoForm(initial=datosMenu)
        return render_to_response('Producto/modificarmenuejecutivo/modificarmenuejecutivo.html',
                                  {'id_menu':id_menu,'formulario': formulario, 'menues': menues, 'plato':platos,
                                   'lista_platos': platos_selec.render(Context({'platos': platosLista})),
                                   'lista_platos_sesion': platos_selec_sesion.render(Context({'platos': platosLista_sesion}))
                                  }, context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarmenudel(request, id_menu):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unMenu = Ejecutivo.objects.get(pk=id_menu)
    except:
        unMenu = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unMenu != None:

        if unMenu.activo:
            unMenu.activo = False
        else:
            unMenu.activo = True

        unMenu.save()

    return HttpResponseRedirect(reverse('modificarmenuejecutivo'))





@permission_required('Administrador.is_admin', login_url="login")
def agregarProductoListaAjax(request):

    platos = None

    if request.method == 'GET':

        id_prod = request.GET['id_prod']

        try:
            lista = request.session['listaProductosModificarMenuEjecutivo']
        except:
            lista =[]

        if id_prod.isdigit():

            listaPlatos =[]

            try:
                lista.remove(id_prod)
            except:
                lista.append(id_prod)

            #lista.append(id_prod)
            request.session['listaProductosModificarMenuEjecutivo']=lista

            for p in lista:
                listaPlatos.append(Plato.objects.get(pk=p))

            platos = listaPlatos

    return render_to_response('Producto/modificarmenuejecutivo/menuejecutivo_platos_ajax.html', {'platos': platos},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        platos_lista = Plato.objects.all().order_by('nombre')
        paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS_MENUES)

        try:
            platos = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            platos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            platos = paginator.page(paginator.num_pages)

        return render_to_response('Producto/modificarmenuejecutivo/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def borrarSesionAjax(request):

    if request.method == 'GET':

        try:
            request.session['listaProductosModificarMenuEjecutivo']=[]
        except:
            return HttpResponse("500")

        return HttpResponse("200")

    else:
        return HttpResponse("500")



@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by('nombre')[:30]

        return render_to_response('Producto/modificarmenuejecutivo/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            platos = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre')
        else:
            platos_lista = Plato.objects.all().order_by("nombre")
            paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS_MENUES)
            platos = paginator.page(1)

        return render_to_response('Producto/modificarmenuejecutivo/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))


