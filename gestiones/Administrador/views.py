from django.contrib.auth.decorators import permission_required
#from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
	
#@login_required()
@permission_required('Administrador.is_admin', login_url="logout")
def Administrador(request):
	return render_to_response('Administrador/administrador.html', {'user': request.user}, context_instance=RequestContext(request))

