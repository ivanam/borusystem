import datetime
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from boru.settings import PAGINADO_PRODUCTOS, STATIC_URL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from gestiones.Comanda.comanda.models import Comanda, Preticket, Factura
from gestiones.Producto.producto.models import Plato, Bebida, DelDia, Ejecutivo


@permission_required('Administrador.is_cajero', login_url="login")
def Cajero(request,pagina=1):

    if pagina == None:
        pagina = 1

    #calculo fecha para filtrar las comandas y dejar las de hoy y ayer nomas
    hoy = datetime.date.today();
    ayer = datetime.date.today()-datetime.timedelta(days=1)

    comandas_lista = Comanda.objects.filter(tipo_comanda__exact="C", finalizada = True,fecha__range=(ayer,hoy),preticket__exact =None).order_by("-fecha", "-hora")
    paginator = Paginator(comandas_lista, PAGINADO_PRODUCTOS)
    comandas = paginator.page(pagina)

    #abro el modelo de comanda abierta
    detalle_comanda=get_template('Cajero/item_comanda_abierta.html')
    #renderizo el template html
    detalle_renderizado=detalle_comanda.render(Context({'comandas': comandas,'STATIC_URL':STATIC_URL}))
    return render_to_response('Cajero/cajero.html', {"item_comandas_abiertas": detalle_renderizado,"titulo":"Comandas","activar_comandas":True}, context_instance=RequestContext(request))


def pretickets(request,pretickets_page=1):
    if pretickets_page == None:
        pretickets_page = 1


    #calculo fecha para filtrar los pedidos y dejar los de hoy y ayer nomas
    hoy = datetime.date.today();
    ayer = datetime.date.today() - datetime.timedelta(days=1)

    pretickets_lista = Preticket.objects.filter(fecha__range=(ayer,hoy)).order_by("-fecha", "-hora")
    paginator = Paginator(pretickets_lista, PAGINADO_PRODUCTOS)
    pretickets = paginator.page(pretickets_page)

    #abro el modelo de comanda abierta
    detalle_preticket = get_template('Cajero/item_preticket.html')
    #renderizo el template html
    detalle_renderizado = detalle_preticket.render(Context({'pretickets': pretickets, 'STATIC_URL': STATIC_URL}))

    return render_to_response('Cajero/cajero.html',
                              {"item_pretickets": detalle_renderizado, "titulo": "Pretickets","activar_pretickets":True},
                              context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def una_comanda(request,id_comanda=None):

    try:
        una_comanda = Comanda.objects.get(pk=id_comanda)

        #abro los modelos
        detalle_generico = get_template('Cajero/resultados_buscador.html')
        detalle_comanda_abierta = get_template('Cajero/item_comanda_abierta.html')
        detalle_pedido = get_template('Cajero/item_pedido_pub.html')
        detalle_preticket = get_template('Cajero/item_preticket.html')
        plantillas = []

        comandas_lista = []
        #si es un pedido
        if una_comanda.tipo_comanda == "P":
            comandas_lista.append(una_comanda)
            plantillas.append(detalle_pedido.render(
                Context({'pedidos': comandas_lista, 'STATIC_URL': STATIC_URL, 'fecha_del_dia': una_comanda.fecha})))
        else:
            #si hay preticket asociado lo muestro
            if una_comanda.preticket != None:
                comandas_lista = []
                comandas_lista.append(una_comanda.preticket)
                plantillas.append(
                    detalle_preticket.render(Context({'pretickets': comandas_lista, 'STATIC_URL': STATIC_URL, 'fecha_del_dia': una_comanda.fecha})))
            else:
                comandas_lista.append(una_comanda)
                plantillas.append(detalle_comanda_abierta.render(
                    Context(
                        {'comandas': comandas_lista, 'STATIC_URL': STATIC_URL, 'fecha_del_dia': una_comanda.fecha})))

        return render_to_response('Cajero/cajero.html',
                              {"una_comanda": detalle_generico.render(Context({'plantillas': plantillas})),
                               "titulo": "Comanda Seleccionada"}, context_instance=RequestContext(request))


    except Exception:
            return HttpResponse("Error, la comanda no fue encontreda en el Systema")








@permission_required('Administrador.is_cajero', login_url="login")
def buscar_mesa(request):

    if request.method == "POST":
        numero = request.POST['numero']

        if numero.isdigit():

            #calculo fecha para filtrar las comandas
            hoy = datetime.date.today();
            ayer = datetime.date.today() - datetime.timedelta(days=1)

            lista_comandas=Comanda.objects.filter(mesas__id=numero,fecha__range=(ayer,hoy)).order_by("-fecha", "-hora")

            #abro los modelos
            detalle_generico = get_template('Cajero/resultados_buscador.html')
            detalle_comanda_abierta = get_template('Cajero/item_comanda_abierta.html')
            detalle_pedido = get_template('Cajero/item_pedido_pub.html')
            detalle_preticket=get_template('Cajero/item_preticket.html')
            plantillas=[]

            for c in lista_comandas:

                comandas_lista=[]
                #si es un pedido
                if c.tipo_comanda == "P":
                    comandas_lista.append(c)
                    plantillas.append(detalle_pedido.render(Context({'pedidos': comandas_lista, 'STATIC_URL': STATIC_URL, 'fecha_del_dia': c.fecha})))
                else:
                    #si hay preticket asociado lo muestro
                    if c.preticket != None:
                        comandas_lista=[]
                        comandas_lista.append(c.preticket)
                        plantillas.append(detalle_preticket.render(Context({'pretickets': comandas_lista, 'STATIC_URL': STATIC_URL, 'fecha_del_dia': c.fecha})))
                    else: #si no hay reticket y no es un pedido, es una comanda abierta
                        comandas_lista.append(c)
                        plantillas.append(detalle_comanda_abierta.render(
                            Context({'comandas': comandas_lista, 'STATIC_URL': STATIC_URL, 'fecha_del_dia': c.fecha})))

            return render_to_response('Cajero/cajero.html',
                                      {"resultados_busqueda": detalle_generico.render(Context({'plantillas': plantillas})), "titulo": "Resultados de la Busqueda"},context_instance=RequestContext(request))
        else:
            return render_to_response('Cajero/cajero.html',
                                      {"resultados_busqueda": "Ingrese un numero de mesa!", "titulo": "Resultados de la Busqueda"},
                                      context_instance=RequestContext(request))
    else:

        return HttpResponse("Error busqueda")

@permission_required('Administrador.is_cajero', login_url="login")
def detalle_comanda_ajax(request):
    if request.method == "GET":
        id_comanda = request.GET["id_comanda"]
        comanda = Comanda.objects.get(pk=id_comanda)
        total = comanda.total()

        return render_to_response('Cajero/detalle_comanda.html', {'comanda': comanda,'total':total},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def detalle_preticket_ajax(request):
    if request.method == "GET":
        id_preticket = request.GET["id_preticket"]
        preticket = Preticket.objects.get(pk=id_preticket)
        total = preticket.total_preticket

        return render_to_response('Cajero/detalle_preticket.html', {'preticket': preticket,'total':total},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_cajero', login_url="login")
def editar_detalle_preticket_ajax(request):
    if request.method == "GET":
        id_preticket = request.GET["id_preticket"]
        preticket = Preticket.objects.get(pk=id_preticket)
        total = preticket.total_preticket

        return render_to_response('Cajero/editar_detalle_preticket.html', {'preticket': preticket,'total':total},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_cajero', login_url="login")
def detalle_factura_ajax(request):
    if request.method == "GET":
        id_factura = request.GET["id_factura"]
        factura = Factura.objects.get(pk=id_factura)
        total = factura.total_factura
        print(factura.total_factura)
        return render_to_response('Cajero/detalle_factura.html', {'factura': factura,'total':total},
                                  context_instance=RequestContext(request))



@permission_required('Administrador.is_cajero', login_url="login")
def pedidos_pub(request, pedidos_page=1):


    if pedidos_page == None:
        pedidos_page = 1

    hoy = datetime.date.today();
    ayer = datetime.date.today() - datetime.timedelta(days=1)

    pedidos_lista = Comanda.objects.filter(tipo_comanda__exact="P", finalizada = True, fecha__range=(ayer, hoy)).order_by("-fecha", "-hora")

    paginator = Paginator(pedidos_lista, PAGINADO_PRODUCTOS)
    pedidos = paginator.page(pedidos_page)

    #abro el modelo de pedido
    detalle_pedido = get_template('Cajero/item_pedido_pub.html')
    #renderizo el template html
    detalle_renderizado = detalle_pedido.render(Context({'pedidos': pedidos}))

    return render_to_response('Cajero/cajero.html',
                              {"item_pedidos_pub": detalle_renderizado, "titulo": "Pedidos Pub","activar_pedidos":True},
                              context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def polling_comandas(request):
    if request.method == "GET":

        hoy = datetime.date.today()
        ayer = datetime.date.today() - datetime.timedelta(days=1)

        comandas_nuevas=Comanda.objects.filter(tipo_comanda__exact="C",vista=False,finalizada=True,cerrada=False, fecha__range=(ayer, hoy)).count()
        pedidos_nuevos =Comanda.objects.filter(tipo_comanda__exact="P",vista=False,finalizada=True,cerrada=True, fecha__range=(ayer, hoy)).count()

    return render_to_response('Cajero/comandas_nuevas.html',{'numero':comandas_nuevas,'numero_pedido':pedidos_nuevos},context_instance=RequestContext(request))


@permission_required('Administrador.is_cajero', login_url="login")
def comanda_vista(request):
    if request.method == "GET":
        id_comanda=request.GET['id_comanda']

        comandas = Comanda.objects.get(pk=id_comanda)
        comandas.vista = True
        comandas.save()
        return HttpResponse("ok")


@permission_required('Administrador.is_cajero', login_url="login")
def cerrar_comanda(request, id_comanda=None):

    comanda = Comanda.objects.get(pk=id_comanda)
    comanda.cerrada = True
    comanda.save()
    generar_preticket(request,id_comanda)
    return HttpResponseRedirect(reverse('una_comanda',args=[id_comanda]))



@permission_required('Administrador.is_cajero', login_url="login")
def generar_preticket(request,id_comanda=None):

    comanda = Comanda.objects.get(pk=id_comanda)
    comanda.estrategia.generar_preticket(comanda)

    return HttpResponseRedirect(reverse('una_comanda', args=[id_comanda]))


@permission_required('Administrador.is_cajero', login_url="login")
def generar_factura(request, id_preticket=None,id_comanda=None):

    preticket = Preticket.objects.get(pk=id_preticket)
    preticket.generar_factura()
    print("preti coma id")
    print(id_comanda)

    return HttpResponseRedirect(reverse('una_comanda', args=[id_comanda]))

@permission_required('Administrador.is_cajero', login_url="login")
def pagar_factura(request, id_factura=None,id_comanda=None):

        factura = Factura.objects.get(pk=id_factura)
        factura.realizar_pago()

        return HttpResponseRedirect(reverse('una_comanda', args=[id_comanda]))

@permission_required('Administrador.is_cajero', login_url="login")
def guardar_detalle_preticket_ajax(request):

    if request.method == "POST":

        #recupero las ids de los platos que quiero agregar al menu
        lista_productos= request.POST.getlist('producto')
        id_prod=0
        categoria=''
        cantidad=0
        #las recorro y rescato los platos y los asigno al menu
        for p in lista_productos:
            #menu.platos.add(Plato.objects.get(pk=p))
            cad = p.split("_")
            id_prod = cad[0]
            categoria = cad[1]
            cantidad = cad[2]

            print id_prod
            print categoria
            print cantidad

    return HttpResponseRedirect(reverse('pretickets'))



@permission_required('Administrador.is_cajero', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        #listado = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by('nombre').filter(activo = True)

        resultados=[]

        platos = Plato.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        bebidas = Bebida.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        delDia = DelDia.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        ejecutivo = Ejecutivo.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        resultados.extend(platos)
        resultados.extend(bebidas)
        resultados.extend(delDia)
        resultados.extend(ejecutivo)

        return render_to_response('Cajero/busquedaresultados.html', {'listado': resultados},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        resultados = []

        if q != "":
            platos = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre').filter(activo = True)

            bebidas = Bebida.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre').filter(activo = True)

            delDia = DelDia.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre').filter(activo = True)

            ejecutivo = Ejecutivo.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('nombre').filter(activo = True)

            resultados.extend(platos)
            resultados.extend(bebidas)
            resultados.extend(delDia)
            resultados.extend(ejecutivo)


        return render_to_response('Cajero/busquedaresultados_items.html', {'plato': resultados},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        platos_lista = Plato.objects.all().order_by('-activo')
        paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)

        try:
            platos = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            platos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            platos = paginator.page(paginator.num_pages)

        return render_to_response('Cajero/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))

