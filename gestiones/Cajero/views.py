from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@permission_required('Administrador.is_cajero', login_url="logout")
def Cajero(request):
	return render_to_response('Cajero/cajero.html', {'user': request.user}, context_instance=RequestContext(request))

