from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from boru.settings import PAGINADO_PRODUCTOS, STATIC_URL
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from gestiones.Comanda.comanda.models import Comanda, EstrategiaPedido


@permission_required('Administrador.is_cajero', login_url="login")
def Cajero(request,pagina=1):

    if pagina == None:
        pagina = 1

    #filtar entre el dia actual y la madrugada del siguiente
    comandas_lista = Comanda.objects.filter(cerrada=False).order_by("-fecha", "-hora")
    paginator = Paginator(comandas_lista, PAGINADO_PRODUCTOS)
    comandas = paginator.page(pagina)

    #abro el modelo de comanda abierta
    detalle_comanda=get_template('Cajero/item_comanda_abierta.html')
    #renderizo el template html
    detalle_renderizado=detalle_comanda.render(Context({'comandas': comandas,'STATIC_URL':STATIC_URL}))

    return render_to_response('Cajero/cajero.html', {"item_comandas_abiertas": detalle_renderizado,"titulo":"Comandas Abiertas"}, context_instance=RequestContext(request))



@permission_required('Administrador.is_cajero', login_url="login")
def detalle_comanda_ajax(request):
    if request.method == "GET":
        id_comanda = request.GET["id_comanda"]
        comanda = Comanda.objects.get(pk=id_comanda)
        total = comanda.total()

        return render_to_response('Cajero/detalle_comanda.html', {'comanda': comanda,'total':total},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def pedidos_pub(request):

    lista_pedidos=[]
    pedidos= Comanda.objects.filter(cerrada=True).order_by("-fecha", "-hora")

    for p in pedidos:
        if type(p.estrategia) is EstrategiaPedido:
            lista_pedidos.append(p)

    #abro el modelo de pedido
    detalle_pedido = get_template('Cajero/item_pedido_pub.html')
    #renderizo el template html
    detalle_renderizado = detalle_pedido.render(Context({'pedidos': lista_pedidos}))

    return render_to_response('Cajero/cajero.html',
                              {"item_pedidos_pub": detalle_renderizado, "titulo": "Pedidos Pub"},
                              context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def polling_comandas(request):
    if request.method == "GET":
        comandas_nuevas=Comanda.objects.filter(cerrada=False,vista=False).count()
        return render_to_response('Cajero/comandas_nuevas.html',{'numero':comandas_nuevas},context_instance=RequestContext(request))


@permission_required('Administrador.is_cajero', login_url="login")
def comanda_vista(request):
    if request.method == "GET":
        id_comanda=request.GET['id_comanda']

        comandas = Comanda.objects.get(pk=id_comanda)
        comandas.vista = True
        comandas.save()
        return HttpResponse("ok")