from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Comanda.comanda.models import Comanda


@permission_required('Administrador.is_cajero', login_url="logout")
def Cajero(request):

    comandas = Comanda.objects.filter(cerrada=False).order_by("-fecha","-hora") #filtar entre el dia actual y la madrugada del siguiente


    return render_to_response('Cajero/cajero.html', {"comandas": comandas}, context_instance=RequestContext(request))

