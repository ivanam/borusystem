# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from boru.settings import PAGINADO_PRODUCTOS
from .forms import modificarusuarioForm
from django.core.urlresolvers import reverse
from gestiones.Administrador.models import permisosVistas


@permission_required('Administrador.is_admin', login_url="login")
def modificarusuarios(request, id_user=None):

    #rescato los usuarios
    user_lista = User.objects.all().exclude(username__icontains = 'admin').order_by('username')
    paginator = Paginator(user_lista, PAGINADO_PRODUCTOS)
    usuarios = paginator.page(1)

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuarioUser = User.objects.get(pk=id_user)

        #creo diccionario con los datos del usuario para mostrarlos ne el formulario
        datosUser = {'id': usuarioUser.id, 'username': usuarioUser.username, 'first_name': usuarioUser.first_name,
                     'last_name': usuarioUser.last_name, 'email': usuarioUser.email, 'tipoDoc': usuarioUser.tipoDoc,
                     'numeroDoc': usuarioUser.numeroDoc, 'telefono': usuarioUser.telefono,
                     'direccion': usuarioUser.direccion,
                     'turno': usuarioUser.turno, 'is_active': usuarioUser.is_active,
                     'permisos':usuarioUser.user_permissions.all()}
    except:
        datosUser = ''
        usuarioUser=None

    #si se apreto el boton de modificar
    if request.method == 'POST' and usuarioUser != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarusuarioForm(request.POST, instance=usuarioUser)

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

            permisos = formulario.cleaned_data['permisos']

            print permisos

            #borro permisos que tenia
            usuarioUser.user_permissions = []
            usuarioUser.save()

            for per in permisos.all():

                #le asigno los nuevos permisos
                if per.codename == "is_admin":

                    #rescato todos los permisos
                    content_type = ContentType.objects.get_for_model(permisosVistas)
                    permisosAll = Permission.objects.filter(content_type=content_type, codename__icontains='is_')

                    #le asigno todos los permisos al user recien creado
                    for p in permisosAll.all():
                        usuarioUser.user_permissions.add(p)

                    usuarioUser.is_superuser = True
                    usuarioUser.is_staff = True
                    usuarioUser.save()

                    break;

                else:

                    usuarioUser.user_permissions.add(per)
                    usuarioUser.is_superuser = False
                    usuarioUser.is_staff = False
                    usuarioUser.save()



            #seteo los nuevos datos en el objeto usuarioUser que obtuvimos al principio
            usuarioUser.username = usuario
            usuarioUser.password = pcontrasenia
            usuarioUser.email = email
            usuarioUser.first_name = nombre
            usuarioUser.last_name = apellido
            usuarioUser.tipoDoc = tipoDoc
            usuarioUser.numeroDoc = numeroDoc
            usuarioUser.telefono = telefono
            usuarioUser.direccion = direccion
            usuarioUser.turno = turno
            usuarioUser.is_active = activo
            usuarioUser.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/modificarusuarios/modificarusuariosexito.html',
                                      {'formulario': formulario, 'usuarios': usuarios},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Administrador/modificarusuarios/modificarusuarios.html',
                                  {'formulario': formulario, 'usuarios': usuarios},
                                  context_instance=RequestContext(request))

    else:
        #si no apretamos el boton modificar  y seleccionamos algun user mostramos sus datos, sino mostramos el form vacio
        formulario = modificarusuarioForm(initial=datosUser)
        return render_to_response('Administrador/modificarusuarios/modificarusuarios.html',
                                  {'formulario': formulario, 'usuarios': usuarios},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificaruserdel(request, id_user):

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuarioUser = User.objects.get(pk=id_user)
    except:
        usuarioUser=None

    #si se apreto el boton de modificar
    if request.method == 'GET' and usuarioUser != None:

        usuarioUser.cambiarEstado()
        usuarioUser.save()

    return HttpResponseRedirect(reverse('modificarusuarios'))


@permission_required('Administrador.is_admin', login_url="login")
def buscaruserajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = User.objects.filter( (Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))).exclude(username__icontains = 'admin').order_by('username','-is_active')[:30]

        return render_to_response('Administrador/modificarusuarios/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscaruserajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            usuarios = User.objects.filter( (Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))).exclude(username__icontains = 'admin').order_by('-is_active')
        else:
            user_lista = User.objects.all().exclude(username__icontains = 'admin').order_by('username')
            paginator = Paginator(user_lista, PAGINADO_PRODUCTOS)
            usuarios = paginator.page(1)

        return render_to_response('Administrador/modificarusuarios/busquedaresultados_items.html', {'usuarios': usuarios},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        user_lista = User.objects.all().exclude(username__icontains = 'admin').order_by('username')
        paginator = Paginator(user_lista, PAGINADO_PRODUCTOS)

        try:
            usuarios = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            usuarios = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            usuarios = paginator.page(paginator.num_pages)

        return render_to_response('Administrador/modificarusuarios/busquedaresultados_items.html', {'usuarios': usuarios},
                                  context_instance=RequestContext(request))

