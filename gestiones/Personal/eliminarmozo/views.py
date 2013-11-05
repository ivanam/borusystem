from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import request, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

@permission_required('Administrador.is_admin', login_url="login")
def eliminarmozoFiltro(request):

    if request.method == "POST":
        filtro = request.POST['q']

        mozos = User.objects.filter(user_permissions__codename="is_mozo").filter(
        Q(first_name__icontains=filtro) | Q(last_name__icontains=filtro) | Q(
            username__icontains=filtro) | Q(
            numeroDoc__icontains=filtro)).order_by('-is_active')

    return render_to_response('Personal/eliminarmozo/eliminarmozo.html', {'mozos': mozos},
                                  context_instance=RequestContext(request))





class eliminarmozo(TemplateView):
    @method_decorator(permission_required('Administrador.is_admin', login_url="login"))
    def dispatch(self, *args, **kwargs):
        return super(eliminarmozo, self).dispatch(*args, **kwargs)

    template_name = 'Personal/eliminarmozo/eliminarmozo.html'
    filtro = ''

    def get_context_data(self):
        context = super(eliminarmozo, self).get_context_data()
        context['mozos'] = User.objects.filter(user_permissions__codename="is_mozo").order_by('-is_active')
        return context

    def post(self, *args, **kwargs):

        mozosId = self.request.POST.getlist('chkId')

        for id in mozosId:

            try:
                usuarioMozo = User.objects.get(pk=id)

                if usuarioMozo.is_active:
                    usuarioMozo.is_active = False
                else:
                    usuarioMozo.is_active = True

                usuarioMozo.save()

            except:
                pass

        return HttpResponseRedirect(reverse('eliminarmozo'))


@permission_required('Administrador.is_admin', login_url="login")
def buscarmozoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = User.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) | Q(numeroDoc__icontains=q)).filter(user_permissions__codename="is_mozo")[:15]

        return render_to_response('Personal/eliminarmozo/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def eliminarmozodel(request, id_user):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuarioMozo = User.objects.get(pk=id_user)
    except:
        usuarioMozo = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and usuarioMozo != None:

        if usuarioMozo.is_active:
            usuarioMozo.is_active = False
        else:
            usuarioMozo.is_active = True

        usuarioMozo.save()

    return HttpResponseRedirect(reverse('eliminarmozo'))