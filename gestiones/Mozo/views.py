from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    return render_to_response('Mozo/mozo.html', {}, context_instance=RequestContext(request))

