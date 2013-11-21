from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from gestiones.Comanda.comanda.models import Comanda


@permission_required('Administrador.is_cajero', login_url="login")
def Cajero(request):
    #filtar entre el dia actual y la madrugada del siguiente
    comandas = Comanda.objects.filter(cerrada=False).order_by("-fecha", "-hora")

    return render_to_response('Cajero/cajero.html', {"comandas": comandas}, context_instance=RequestContext(request))

@permission_required('Administrador.is_cajero', login_url="login")
def detalle_comanda_ajax(request):
    if request.method == "GET":
        id_comanda = request.GET["id_comanda"]
        comanda = Comanda.objects.get(pk=id_comanda)
        #detalle_comanda = get_template('Cajero/detalle_comanda.html')
        return render_to_response('Cajero/detalle_comanda.html', {'comanda': comanda},
                                  context_instance=RequestContext(request))
