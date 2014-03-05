from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


def Index(request):

    """if not request.user.is_anonymous():
        return HttpResponseRedirect(request.path)
        print request.path
        pass
    """
    if request.method == 'POST':

        formulario = AuthenticationForm(request.POST)

        if formulario.is_valid:

            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)

            if acceso is not None:

                if acceso.is_active:

                    login(request, acceso)
                    permisosUser = acceso.get_all_permissions()

                    if 'Administrador.is_admin' in permisosUser:
                        return HttpResponseRedirect('administrador')

                    if 'Administrador.is_cajero' in permisosUser:
                        return HttpResponseRedirect('cajero')

                    if 'Administrador.is_mozo' in permisosUser:
                        return HttpResponseRedirect('mozo')

                else:
                    return render_to_response('Index/index.html', {'mostrarError': True},
                                              context_instance=RequestContext(request))

            else:
                return render_to_response('Index/index.html', {'mostrarError': True},
                                          context_instance=RequestContext(request))


    else:
        return render_to_response('Index/index.html', {'mostrarError': False}, context_instance=RequestContext(request))