from django.contrib.auth.decorators import permission_required
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


#@login_required()
#from gestiones.Comanda.comanda.models import EstrategiaComanda
from boru.settings import PAGINADO_USUARIOS
from gestiones.Administrador.forms import altaUsuarioForm
from gestiones.Administrador.models import permisosVistas


@permission_required('Administrador.is_admin', login_url="logout")
def Administrador(request):
    return render_to_response('Administrador/administrador.html', {'user': request.user},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def AltaAdministrador(request):
    if request.method == 'POST':
        formulario = altaUsuarioForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            usuario = formulario.cleaned_data['username']
            contrasenia = formulario.cleaned_data['password']
            email = formulario.cleaned_data['email']
            activo = formulario.cleaned_data['is_active']
            print(activo)

            #creamos el user mozo
            usuarioAdministrador = User.objects.create_user(usuario, email, contrasenia)
            #rescato los permiso de mozo
            content_type = ContentType.objects.get_for_model(permisosVistas)
            permisoMozo = Permission.objects.get(content_type=content_type, codename='is_admin')
            #se los asigno al mozo recien creado
            usuarioAdministrador.user_permissions.add(permisoMozo)
            #Actualizo y guardo al user
            usuarioAdministrador.is_active = activo
            usuarioAdministrador.is_superuser = True
            usuarioAdministrador.is_staff = True

            usuarioAdministrador.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/altaAdministradorExito.html', {},
                                      context_instance=RequestContext(request))

        return render_to_response('Administrador/altaAdministrador.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:
        formulario = altaUsuarioForm()
        return render_to_response('Administrador/altaAdministrador.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def AltaCajero(request):
    if request.method == 'POST':
        formulario = altaUsuarioForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            usuario = formulario.cleaned_data['username']
            contrasenia = formulario.cleaned_data['password']
            email = formulario.cleaned_data['email']
            activo = formulario.cleaned_data['is_active']

            #creamos el user mozo
            usuarioCajero = User.objects.create_user(usuario, email, contrasenia)
            #rescato los permiso de mozo
            content_type = ContentType.objects.get_for_model(permisosVistas)
            permisoCajero = Permission.objects.get(content_type=content_type, codename='is_cajero')
            #se los asigno al mozo recien creado
            usuarioCajero.user_permissions.add(permisoCajero)
            #Actualizo y guardo al user
            usuarioCajero.is_active = activo

            usuarioCajero.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/altaCajeroExito.html', {},
                                      context_instance=RequestContext(request))

        return render_to_response('Administrador/altaCajero.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:
        formulario = altaUsuarioForm()
        return render_to_response('Administrador/altaCajero.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def ModificarUsuario(request, id_user=None):
    #rescato los    usarios que son mozos
    usuarios_lista = User.objects.all().order_by('username')
    paginator = Paginator(usuarios_lista, PAGINADO_USUARIOS)
    usuarios = paginator.page(1)

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuario = User.objects.get(pk=id_user)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosUsuario = {'id': usuario.id, 'username': usuario.username, 'email': usuario.email,
                        'is_active': usuario.is_active}
    except:
        datosUsuario = ''
        usuario = None

    #si se apreto el boton de modificar
    if request.method == 'POST' and usuario != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = altaUsuarioForm(request.POST, instance=usuario)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada campo y los limpio
            usuario_username = formulario.cleaned_data['username']
            contrasenia = formulario.cleaned_data['password']

            pcontrasenia = make_password(contrasenia)

            email = formulario.cleaned_data['email']
            activo = formulario.cleaned_data['is_active']

            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            usuario.username = usuario_username
            usuario.password = pcontrasenia
            usuario.email = email
            usuario.is_active = activo
            usuario.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/ModificarUsuarioExito.html',
                                      {'formulario': formulario, 'usuarios': usuarios},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Administrador/ModificarUsuarios.html',
                                  {'formulario': formulario, 'usuarios': usuarios},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = altaUsuarioForm(initial=datosUsuario)
        return render_to_response('Administrador/ModificarUsuarios.html',
                                  {'formulario': formulario, 'usuarios': usuarios},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarUsuariodel(request, id_user):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        usuario = User.objects.get(pk=id_user)
    except:
        usuario = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and usuario != None:
        usuario.cambiarEstado()
        usuario.save()

    return HttpResponseRedirect(reverse('modificarUsuarios'))


@permission_required('Administrador.is_admin', login_url="login")
def buscarUsuariosajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = User.objects.filter((Q(username__icontains=q) )).order_by('username')[:30]
        return render_to_response('Administrador/modificarUsuarioBusquedaResultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarUsuariosajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            usuarios = User.objects.filter((Q(username__icontains=q) )).order_by('username')
        else:
            usuarios_lista = User.objects.filter().order_by('username')
            paginator = Paginator(usuarios_lista, PAGINADO_USUARIOS)
            usuarios = paginator.page(1)

        return render_to_response('Administrador/modificarUsuarioBusquedaResultados_items.html', {'usuarios': usuarios},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):
    if request.method == 'GET':

        pagina = request.GET['pagina']
        usuario_lista = User.objects.filter().order_by('username')
        paginator = Paginator(usuario_lista, PAGINADO_USUARIOS)

        try:
            usuarios = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            usuarios = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            usuarios = paginator.page(paginator.num_pages)

        return render_to_response('Administrador/modificarUsuarioBusquedaResultados_items.html', {'usuarios': usuarios},
                                  context_instance=RequestContext(request))
