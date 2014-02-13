from cookielib import http2time
import datetime
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, response, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from fpdf import FPDF
import xlsxwriter

from boru.settings import PAGINADO_USUARIOS, STATIC_URL, RUTA_PROYECTO
from gestiones.Administrador.forms import altaUsuarioForm, fechasXconsultaForm
from gestiones.Administrador.models import permisosVistas
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Comanda.comanda.models import Factura
from gestiones.Producto.producto.models import Plato, Bebida, Ejecutivo, DelDia


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


@permission_required('Administrador.is_admin', login_url="login")
def listarImprimir(request):
    fecha = datetime.date.today()
    now = datetime.datetime.now()
    nombre = str(fecha) + str(now.hour) + str(now.minute) + str(now.second) + '.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'BU', 25)

    pdf.image(RUTA_PROYECTO + "\\" + STATIC_URL + "img\\boru_logo_pdf.png", 13, 13, 52, 23, type='PNG')
    pdf.cell(0, 30, 'Carta Boru', 0, 1, 'C')
    pdf.ln(10)

    secciones = SeccionCarta.objects.filter().order_by("categoria")
    for seccion in secciones:
        if not seccion.es_vacia_seccion():
            pdf.set_font('Arial', 'UB', 20)
            pdf.cell(0, 10, str(seccion.nombre).capitalize(), 0, 1, 'L')

            productos = seccion.dame_productos()
            for p in productos:
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(75, 10, str(p.nombre).capitalize(), 0, 0)

                pdf.set_font('Arial', 'B', 16)
                pdf.cell(90, 10, "........................................................", 0, 0, "L")

                pdf.set_font('Arial', 'B', 16)
                pdf.cell(25, 10, '$' + str(p.importe()), 0, 0, "L")
                pdf.ln()
            pdf.ln()

    nombre = RUTA_PROYECTO + "\\" + STATIC_URL + "pdf\\" + nombre
    nombreWeb = STATIC_URL + "pdf\\" + nombre
    pdf.output(name=nombre, dest='F')


    #exel ejemplo
    workbook = xlsxwriter.Workbook(RUTA_PROYECTO + "\\" + STATIC_URL + "xlsx\\grafico.xlsx")
    worksheet = workbook.add_worksheet()
    # Add the worksheet data to be plotted.
    platos_stock = Plato.objects.all().order_by("-stock")[0:5]
    bebidas_stock = Bebida.objects.all().order_by("-stock")[0:5]
    menue_stock = Ejecutivo.objects.all().order_by("-stock")[0:5]
    menud_stock = DelDia.objects.all().order_by("-stock")[0:5]

    platos = []
    data = []
    nombre = []

    platos.extend(platos_stock)
    platos.extend(bebidas_stock)
    platos.extend(menue_stock)
    platos.extend(menud_stock)

    for p in platos:
        data.append(p.stock)
        nombre.append(p.nombre)

    worksheet.write_column('A1', nombre)
    worksheet.write_column('B1', data)
    # Create a new chart object.
    chart = workbook.add_chart({'type': 'pie'})
    # Add a series to the chart.
    chart.add_series({'values': '=Sheet1!$B$1:$B$' + str(len(data))})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('D1', chart)
    workbook.close()

    return render_to_response('Administrador/visorPdf.html', {'nombre': nombreWeb},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def masVendidos(request):
    if request.method == 'POST':
        formulario = fechasXconsultaForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            fechaI = formulario.cleaned_data['fecha_Inicio']
            fechaF = formulario.cleaned_data['fecha_fin']

            facturas = Factura.objects.filter(fecha__range=(fechaI, fechaF))
            for f in facturas:
                if (f.comanda != None):
                    print (f.comanda)
                else:
                    print (f.preticket)

            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/consultaMasVendidoMsj.html', {},
                                      context_instance=RequestContext(request))

        return render_to_response('Administrador/consultaMasVendido.html',
                                  {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:
        formulario = fechasXconsultaForm()
        return render_to_response('Administrador/consultaMasVendido.html',
                                  {'formulario': formulario},
                                  context_instance=RequestContext(request))

