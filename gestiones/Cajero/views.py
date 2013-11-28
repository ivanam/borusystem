import datetime
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from boru.settings import PAGINADO_PRODUCTOS, STATIC_URL
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
import estrategia
from gestiones.Comanda.comanda.models import Comanda, EstrategiaPedido, Preticket, Factura


@permission_required('Administrador.is_cajero', login_url="login")
def Cajero(request,pagina=1):

    if pagina == None:
        pagina = 1

    #TODO tratar de filtrar las comandas y dejar las de hoy y ayer nomas
    comandas_lista = Comanda.objects.filter(tipo_comanda__exact="C", finalizada = True, cerrada = False).order_by("-fecha", "-hora")
    paginator = Paginator(comandas_lista, PAGINADO_PRODUCTOS)
    comandas = paginator.page(pagina)

    #abro el modelo de comanda abierta
    detalle_comanda=get_template('Cajero/item_comanda_abierta.html')
    #renderizo el template html
    detalle_renderizado=detalle_comanda.render(Context({'comandas': comandas,'STATIC_URL':STATIC_URL}))

    print(detalle_renderizado)
    return render_to_response('Cajero/cajero.html', {"item_comandas_abiertas": detalle_renderizado,"titulo":"Comandas Abiertas"}, context_instance=RequestContext(request))


def comandas_cerradas(request,comandacerrada=1):
    if comandacerrada == None:
        comandacerrada = 1

    #TODO tratar de filtrar las comandas y dejar las de hoy y ayer nomas
    comandas_lista = Comanda.objects.filter(tipo_comanda__exact="C", finalizada=True, cerrada=True).order_by("-fecha", "-hora")
    paginator = Paginator(comandas_lista, PAGINADO_PRODUCTOS)
    comandas = paginator.page(comandacerrada)

    #abro el modelo de comanda abierta
    detalle_comanda = get_template('Cajero/item_comanda_cerrada.html')
    #renderizo el template html
    detalle_renderizado = detalle_comanda.render(Context({'comandas': comandas, 'STATIC_URL': STATIC_URL}))

    return render_to_response('Cajero/cajero.html',
                              {"item_comandas_cerradas": detalle_renderizado, "titulo": "Comandas Cerradas"},
                              context_instance=RequestContext(request))



def pretickets(request,pretickets_page=1):
    if pretickets_page == None:
        pretickets_page = 1

    #TODO tratar de filtrar los pretickets y dejar las de hoy y ayer nomas
    pretickets_lista = Preticket.objects.all().order_by("-fecha", "-hora")
    paginator = Paginator(pretickets_lista, PAGINADO_PRODUCTOS)
    pretickets = paginator.page(pretickets_page)

    #abro el modelo de comanda abierta
    detalle_preticket = get_template('Cajero/item_preticket.html')
    #renderizo el template html
    detalle_renderizado = detalle_preticket.render(Context({'pretickets': pretickets, 'STATIC_URL': STATIC_URL}))

    return render_to_response('Cajero/cajero.html',
                              {"item_pretickets": detalle_renderizado, "titulo": "Pretickets"},
                              context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def buscar_mesa(request):

    if request.method == "POST":
        numero = request.POST['numero']

        if numero.isdigit():
            lista_comandas=Comanda.objects.filter(mesas__id=numero).order_by("-fecha", "-hora")

            #abro los modelos
            detalle_generico = get_template('Cajero/resultados_buscador.html')
            detalle_comanda_abierta = get_template('Cajero/item_comanda_abierta.html')
            detalle_comanda_cerrada = get_template('Cajero/item_comanda_cerrada.html')
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

                    #si es una comanda abierta
                    if c.finalizada == True and c.cerrada == False :
                        comandas_lista.append(c)
                        plantillas.append(detalle_comanda_abierta.render(Context({'comandas': comandas_lista, 'STATIC_URL': STATIC_URL,'fecha_del_dia':c.fecha})))

                    else:
                    #si es una comanda cerrada
                        comandas_lista.append(c)
                        plantillas.append(detalle_comanda_cerrada.render(Context({'comandas': comandas_lista, 'STATIC_URL': STATIC_URL,'fecha_del_dia':c.fecha})))

                        #me fijo si tiene preticket
                        hay_preticket=Preticket.objects.filter(comanda__id=c.id)

                        #si encuentro alguno lo muestro
                        if len(hay_preticket) > 0:

                            comandas_lista=[]

                            for p in hay_preticket:
                                comandas_lista.append(p)

                            plantillas.append(detalle_preticket.render(Context({'pretickets': comandas_lista, 'STATIC_URL': STATIC_URL})))


            return render_to_response('Cajero/cajero.html',
                                      {"resultados_busqueda": detalle_generico.render(Context({'plantillas': plantillas})), "titulo": "Resultados de la Busqueda"},context_instance=RequestContext(request))
        else:
            return render_to_response('Cajero/cajero.html',
                                      {"resultados_busqueda": "Ingrese el numero de mesa.", "titulo": "Resultados de la Busqueda"},
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
        total = preticket.total

        return render_to_response('Cajero/detalle_preticket.html', {'preticket': preticket,'total':total},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_cajero', login_url="login")
def detalle_factura_ajax(request):
    if request.method == "GET":
        id_factura = request.GET["id_factura"]
        factura = Factura.objects.get(pk=id_factura)
        total = factura.total

        return render_to_response('Cajero/detalle_factura.html', {'factura': factura,'total':total},
                                  context_instance=RequestContext(request))



@permission_required('Administrador.is_cajero', login_url="login")
def pedidos_pub(request, pedidos_page=1):


    if pedidos_page == None:
        pedidos_page = 1

    #TODO tratar de filtrar los pedidos y dejar las de hoy y ayer nomas
    pedidos_lista = pedidos= Comanda.objects.filter(tipo_comanda__exact="P", finalizada = True).order_by("-fecha", "-hora")

    paginator = Paginator(pedidos_lista, PAGINADO_PRODUCTOS)
    pedidos = paginator.page(pedidos_page)

    #abro el modelo de pedido
    detalle_pedido = get_template('Cajero/item_pedido_pub.html')
    #renderizo el template html
    detalle_renderizado = detalle_pedido.render(Context({'pedidos': pedidos}))

    return render_to_response('Cajero/cajero.html',
                              {"item_pedidos_pub": detalle_renderizado, "titulo": "Pedidos Pub"},
                              context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def polling_comandas(request):
    if request.method == "GET":
        comandas_nuevas=Comanda.objects.filter(tipo_comanda__exact="C",vista=False,finalizada=True,cerrada=False).count()
        pedidos_nuevos =Comanda.objects.filter(tipo_comanda__exact="P",vista=False,finalizada=True,cerrada=True).count()

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
def cerrar_comanda(request):
    if request.method == "GET":
        id_comanda = request.GET['id_comanda']

        comanda = Comanda.objects.get(pk=id_comanda)
        comanda.cerrada=True
        comanda.save()

        return HttpResponse("ok cerrar comanda")


@permission_required('Administrador.is_cajero', login_url="login")
def generar_preticket(request):
    if request.method == "GET":
        id_comanda = request.GET['id_comanda']

        comanda = Comanda.objects.get(pk=id_comanda)
        comanda.estrategia.generar_preticket(comanda)

        return HttpResponse("ok generar preticket")


@permission_required('Administrador.is_cajero', login_url="login")
def generar_factura(request):
    if request.method == "GET":
        id_preticket = request.GET['id_preticket']

        preticket = Preticket.objects.get(pk=id_preticket)
        id_factura = preticket.generar_factura()

        return HttpResponse(id_factura)
