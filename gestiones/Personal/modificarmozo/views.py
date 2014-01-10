# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from boru.settings import PAGINADO_PRODUCTOS
from .forms import modificarMozo
from django.core.urlresolvers import reverse

@permission_required('Administrador.is_admin', login_url="login")
def modificarmozo(request, id_user = None):

    #rescato los    usarios que son mozos
    mozos_lista = User.objects.filter(user_permissions__codename="is_mozo").order_by('username','-is_active')
    paginator = Paginator(mozos_lista, PAGINADO_PRODUCTOS)
    mozos = paginator.page(1)

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuarioMozo = User.objects.get(pk=id_user)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosMozo = {'id': usuarioMozo.id, 'username': usuarioMozo.username, 'first_name': usuarioMozo.first_name,
                     'last_name': usuarioMozo.last_name, 'email': usuarioMozo.email, 'tipoDoc': usuarioMozo.tipoDoc,
                     'numeroDoc': usuarioMozo.numeroDoc, 'telefono': usuarioMozo.telefono,
                     'direccion': usuarioMozo.direccion,
                     'turno': usuarioMozo.turno, 'is_active': usuarioMozo.is_active}
    except:
        datosMozo = ''
        usuarioMozo=None

    #si se apreto el boton de modificar
    if request.method == 'POST' and usuarioMozo != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarMozo(request.POST, instance=usuarioMozo)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada campo y los limpio
            usuario = formulario.cleaned_data['username']
            contrasenia = formulario.cleaned_data['password']

            pcontrasenia = make_password(contrasenia)

            nombre = formulario.cleaned_data['first_name']
            apellido = formulario.cleaned_data['last_name']
            email = formulario.cleaned_data['email']
            tipoDoc = formulario.cleaned_data['tipoDoc']
            numeroDoc = formulario.cleaned_data['numeroDoc']
            telefono = formulario.cleaned_data['telefono']
            direccion = formulario.cleaned_data['direccion']
            turno = formulario.cleaned_data['turno']
            activo = formulario.cleaned_data['is_active']

            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            usuarioMozo.username = usuario
            usuarioMozo.password = pcontrasenia
            usuarioMozo.email = email
            usuarioMozo.first_name = nombre
            usuarioMozo.last_name = apellido
            usuarioMozo.tipoDoc = tipoDoc
            usuarioMozo.numeroDoc = numeroDoc
            usuarioMozo.telefono = telefono
            usuarioMozo.direccion = direccion
            usuarioMozo.turno = turno
            usuarioMozo.is_active = activo
            usuarioMozo.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Personal/modificarmozo/modificarexito.html',
                                      {'formulario': formulario, 'mozos': mozos},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Personal/modificarmozo/modificarmozo.html',
                                  {'formulario': formulario, 'mozos': mozos},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarMozo(initial=datosMozo)
        return render_to_response('Personal/modificarmozo/modificarmozo.html',
                                  {'formulario': formulario, 'mozos': mozos},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarexito(request):
    return render_to_response('Personal/modificarmozo/modificarexito.html', context_instance=RequestContext(request))

@permission_required('Administrador.is_admin', login_url="login")
def modificarmozodel(request, id_user):

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuarioMozo = User.objects.get(pk=id_user)
    except:
        usuarioMozo=None

    #si se apreto el boton de modificar
    if request.method == 'GET' and usuarioMozo != None:

        usuarioMozo.cambiarEstado()
        usuarioMozo.save()

    return HttpResponseRedirect(reverse('modificarmozo'))




@permission_required('Administrador.is_admin', login_url="login")
def buscarmozosajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = User.objects.filter( (Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)),user_permissions__codename="is_mozo").order_by('username','-is_active')[:30]

        return render_to_response('Personal/modificarmozo/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarmozosajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            mozos = User.objects.filter( (Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)),user_permissions__codename="is_mozo").order_by('-is_active')
        else:
            mozos_lista = User.objects.filter(user_permissions__codename="is_mozo").order_by('username','-is_active')
            paginator = Paginator(mozos_lista, PAGINADO_PRODUCTOS)
            mozos = paginator.page(1)

        return render_to_response('Personal/modificarmozo/busquedaresultados_items.html', {'mozos': mozos},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        mozos_lista = User.objects.filter(user_permissions__codename="is_mozo").order_by('username','-is_active')
        paginator = Paginator(mozos_lista, PAGINADO_PRODUCTOS)

        try:
            mozos = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            mozos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            mozos = paginator.page(paginator.num_pages)

        return render_to_response('Personal/modificarmozo/busquedaresultados_items.html', {'mozos': mozos},
                                  context_instance=RequestContext(request))
