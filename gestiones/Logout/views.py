from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def desloguearse(request):
	logout(request)
	return HttpResponseRedirect("/")