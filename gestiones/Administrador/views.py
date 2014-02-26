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
from django.template.loader import render_to_string
from fpdf import FPDF
import xlsxwriter
from gestiones.Administrador.ayudaContextual import ayudaMsg
from boru.settings import PAGINADO_USUARIOS, STATIC_URL, RUTA_PROYECTO, TOTAL_LINEAS_PDF
from gestiones.Administrador.forms import altaUsuarioForm, fechasXconsultaForm, fechasXconsultaFacturasForm
from gestiones.Administrador.models import permisosVistas
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Comanda.comanda.models import Factura, DetalleFactura
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
    lineas = TOTAL_LINEAS_PDF
    fecha = datetime.date.today()
    now = datetime.datetime.now()
    nombre = "Carta_Boru_"+str(fecha)+'.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'BU', 25)
    pdf.image(RUTA_PROYECTO + "\\" + STATIC_URL + "img\\boru_logo_pdf.png", 13, 13, 52, 23, type='PNG')
    pdf.cell(0, 30, 'Carta Boru', 0, 1, 'C')
    pdf.ln(10)
    lineas = lineas - 4
    secciones = SeccionCarta.objects.filter().order_by("categoria")
    for seccion in secciones:
        if not seccion.es_vacia_seccion():
            if (lineas - 3) <= 0:
                pdf.add_page()
                lineas = TOTAL_LINEAS_PDF
            lineas = lineas - 3
            pdf.set_font('Arial', 'UB', 20)
            pdf.cell(0, 10, str(seccion.nombre).capitalize(), 0, 1, 'L')
            pdf.ln()
            productos = seccion.dame_productos()
            for p in productos:
                if p.activo ==True:
                    if (lineas - 2) <= 0:
                        pdf.add_page()
                        lineas = TOTAL_LINEAS_PDF - 3
                        pdf.set_font('Arial', 'UB', 20)
                        pdf.cell(0, 10, str(seccion.nombre).capitalize(), 0, 1, 'L')
                        pdf.ln()
                    lineas= lineas -2
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(75, 10, str(p.nombre).capitalize(), 0, 0)
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(90, 10, "........................................................", 0, 0, "L")
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(25, 10, '$' + str(p.importe()), 0, 0, "L")
                    pdf.ln()
            pdf.ln()
            lineas = lineas -1
    #nombre = RUTA_PROYECTO + "\\" + STATIC_URL + "pdf\\" + nombre
    #nombreWeb = STATIC_URL + "pdf\\" + nombre
    #pdf.output(name=nombre, dest='F')
    #return render_to_response('Administrador/visorPdf.html', {'nombre': nombreWeb},
     #                         context_instance=RequestContext(request))
    return HttpResponse(pdf.output(name=nombre,dest='S'),content_type='application/pdf')


@permission_required('Administrador.is_admin', login_url="login")
def masVendidos(request):
    if request.method == 'POST':
        formulario = fechasXconsultaForm(request.POST)

        if formulario.is_valid():

            #capturamos y limpiamos datos
            fechaI = formulario.cleaned_data['fecha_Inicio']
            fechaF = formulario.cleaned_data['fecha_fin']
            tipo_grafico = formulario.cleaned_data['tipo_grafico']
            producto_informe = formulario.cleaned_data['producto_informe']
            top_productos = formulario.cleaned_data['top_productos']
            criterio_consulta = formulario.cleaned_data['criterio_consulta']

            titulo = 'Productos '

            #parseamos parametros de la consulta
            if criterio_consulta == "MAS":
                order = 'DESC'
                titulo = titulo + 'mas vendidos '
            else:
                order = 'ASC'
                titulo = titulo + 'menos vendidos '

            titulo = titulo + 'entre '+ str(fechaI) +' y '+str(fechaF)+' \n'

            if top_productos != "ALL":
                limite_productos = 'LIMIT ' + str(top_productos)
                titulo = titulo + '(Top ' + str(top_productos)+' '
            else:
                limite_productos = ''
                titulo = titulo + '(Todos '


            if producto_informe == "TODOS":

                titulo = titulo + 'Productos)'

                sql_query = 'select id,nombre, SUM(cantidad) as cant ' \
                            'from comanda_detallefactura ' \
                            'where id in ' \
                            '( select cfd.detallefactura_id ' \
                            'from comanda_factura as cf inner join comanda_factura_detalle as cfd ' \
                            'on cf.id = cfd.factura_id ' \
                            'and cf.fecha between \'' + str(fechaI) + '\' and \'' + str(fechaF) + '\') ' \
                            'group by nombre order by cant ' + order + ' ' + limite_productos + ';'

            else:

                titulo = titulo + str(producto_informe).capitalize() +')'

                sql_query = 'select id,nombre, SUM(cantidad) as cant ' \
                            'from comanda_detallefactura ' \
                            'where id in ' \
                            '( ' \
                            'select j.id from ' \
                                '(' \
                                'select cfd.detallefactura_id from ' \
                                'comanda_factura as cf inner join comanda_factura_detalle as cfd ' \
                                'on cf.id = cfd.factura_id ' \
                                'and cf.fecha between \'' + str(fechaI) + '\' and \'' + str(fechaF) + '\'' \
                                ') ' \
                                'as h inner join ' \
                                    '(' \
                                    'select id from comanda_detallefactura ' \
                                    'where nombre in ' \
                                        '(' \
                                        'select nombre from producto_'+producto_informe+' ' \
                                        ')' \
                                    ') as j on h.detallefactura_id = j.id' \
                                ') ' \
                                'group by nombre order by cant ' + order + ' ' + limite_productos + ';'

            #Generando el grafico en excel
            nombre_archivo = "grafico.xlsx"
            workbook = xlsxwriter.Workbook(RUTA_PROYECTO + "/" + STATIC_URL + "xlsx/" + nombre_archivo)
            worksheet = workbook.add_worksheet()
            data = []
            nombre = []

            format = workbook.add_format()
            format.set_bold()
            format.set_font_size(12)
            #Productos mas vendidos
            worksheet.write('A1', 'Producto',format)
            worksheet.write('B1', 'Cantidad vendida',format)


            for x in DetalleFactura.objects.raw(sql_query):
                data.append(x.cant)
                nombre.append(x.nombre)

            format = workbook.add_format()
            format.set_indent(2)

            worksheet.set_column(0, 0, 40)
            worksheet.write_column('A2', nombre,format)
            worksheet.write_column('B2', data,format)
            # Create a new chart object.
            chart = workbook.add_chart({'type': str(tipo_grafico)})
            chart.set_title({'name': titulo,
                             'name_font': {
                                'name': 'Arial',
                                'color': '#000000',
                                'size': 9,},
                             })
            # Add a series to the chart.

            chart.add_series({
                'values': '=Sheet1!$B$2:$B$' + str(len(data)+1),
                'categories': '=Sheet1!$A$2:$A$' + str(len(nombre)+1)
            })
            # Insert the chart into the worksheet.
            worksheet.insert_chart('D2', chart)
            workbook.close()

            #mostramos que la operacion fue exitosa
            return render_to_response('Administrador/consultaMasVendido.html', {'formulario': formulario,'consulta':True,'nombre_archivo':nombre_archivo},
                                      context_instance=RequestContext(request))

        return render_to_response('Administrador/consultaMasVendido.html',
                                  {'formulario': formulario,'consulta':False},
                                  context_instance=RequestContext(request))

    else:
        formulario = fechasXconsultaForm()
        return render_to_response('Administrador/consultaMasVendido.html',
                                  {'formulario': formulario,'consulta':False},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def ayudaContextual(request):
    if request.method == 'GET':

        try:
            fuente=request.GET['fuente']
            entrada = ayudaMsg.get(fuente, "Ayuda en construccion!")
            titulo = entrada.get("titulo")
            plantilla = entrada.get("plantilla")
            mensaje = entrada.get("msg")

            if plantilla != None:
                plantilla_ayuda = render_to_string('Administrador/ayudaContextual/'+ plantilla, {},
                                                  context_instance=RequestContext(request))
            else:
                plantilla_ayuda = None
        except:
            titulo = "Titulo en construccion!"
            plantilla_ayuda = None
            mensaje = "Mensaje en construccion!"

    return render_to_response('Administrador/ayudaContextual.html', {'titulo': titulo, 'mensaje': mensaje, 'fuente':fuente, 'plantilla':plantilla_ayuda},
                              context_instance=RequestContext(request))

@permission_required('Administrador.is_admin', login_url="login")
def consultaFacturas(request):
    if request.method== 'POST':
        formulario = fechasXconsultaFacturasForm(request.POST)
        #nombre = 'ganancia.xlsx'
        if formulario.is_valid():

            #capturamos y limpiamos datos
            fechaI = formulario.cleaned_data['fecha_Inicio']
            fechaF = formulario.cleaned_data['fecha_fin']
            sql_query = 'select id, fecha, hora, tipo, total_factura ' \
                            'from comanda_factura ' \
                            'where comanda_factura.fecha between \'' + str(fechaI) + '\' and \'' + str(fechaF) + '\''+' and comanda_factura.pago_id IS NOT NULL'+';'

            nombre_archivo = "facturas.xlsx"
            workbook = xlsxwriter.Workbook(RUTA_PROYECTO + "/" + STATIC_URL + "xlsx/" + nombre_archivo)
            worksheet = workbook.add_worksheet()
            fecha = []
            hora = []
            tipo = []
            totalF = []
            id = []
            totalC = 0

            formatT = workbook.add_format()
            formatT.set_bold()
            formatT.set_font_size(14)
            formatT.set_align('center')
            #Facturas
            worksheet.write('A1', 'Numero Factura', formatT)
            worksheet.write('B1', 'Fecha', formatT)
            worksheet.write('C1', 'Hora', formatT)
            worksheet.write('D1', 'Tipo', formatT)
            worksheet.write('E1', 'Total', formatT)
            fila = 2
            for x in Factura.objects.raw(sql_query):
                fecha.append(str(x.fecha))
                hora.append(str(x.hora))
                tipo.append(x.tipo)
                totalF.append(str(x.total_factura))
                id.append(x.id)
                totalC = totalC + x.total_factura
                fila = fila + 1
            fila = fila +1
            format = workbook.add_format()
            format.set_indent(5)

            worksheet.set_column(0, 0, 40)
            worksheet.write_column('A2', id, format)
            worksheet.write_column('B2', fecha, format)
            worksheet.write_column('C2', hora, format)
            worksheet.write_column('D2', tipo, format)
            worksheet.write_column('E2', totalF, format)
            #worksheet.write('F2', str(totalC), format)
            worksheet.write('A'+str(fila), 'Total Facturado de '+str(fechaI)+' a '+str(fechaF),formatT)

            format = workbook.add_format()
            format.set_align('center')
            worksheet.write('E'+str(fila), str(totalC), format)
            #worksheet.write_column('F2', totalC, format)
            # Create a new chart object.
            # Insert the chart into the worksheet.
            #worksheet.insert_chart('D2', chart)
            workbook.close()

            return render_to_response('Administrador/consultaFacturas.html', {'formulario': formulario,'consulta':True,'nombre_archivo':nombre_archivo},
                                      context_instance=RequestContext(request))

    else:
        formulario = fechasXconsultaFacturasForm()
        return render_to_response('Administrador/consultaFacturas.html',
                                  {'formulario': formulario,'consulta':False},
                                  context_instance=RequestContext(request))