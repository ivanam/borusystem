import datetime
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from fpdf import FPDF
import xlsxwriter
from gestiones.Administrador.ayudaContextual import ayudaMsg
from boru.settings import STATIC_URL, RUTA_PROYECTO, TOTAL_LINEAS_PDF
from gestiones.Administrador.forms import  fechasXconsultaForm, fechasXconsultaFacturasForm
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Comanda.comanda.models import Factura, DetalleFactura



@permission_required('Administrador.is_admin', login_url="logout")
def Administrador(request):
    return render_to_response('Administrador/administrador.html', {'user': request.user},
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
            #Formato del titulo
            formatT = workbook.add_format()
            formatT.set_bold()
            formatT.set_font_size(12)
            formatT.set_align('center')
            #Formato para los titulos de la tabla
            formatT2 = workbook.add_format()
            formatT2.set_align('center')
            formatT2.set_font_size(12)
            formatT2.set_bold()
            formatT2.set_bg_color('silver')
            #Facturas
            worksheet.write('C1', 'Facturacion de '+str(fechaI)+' al '+str(fechaF), formatT)
            worksheet.write('A2', 'Numero Factura', formatT2)
            worksheet.write('B2', 'Fecha', formatT2)
            worksheet.write('C2', 'Hora', formatT2)
            worksheet.write('D2', 'Tipo', formatT2)
            worksheet.write('E2', 'Total', formatT2)
            fila = 3 #contador de filas dentro del excel
            for x in Factura.objects.raw(sql_query):
                fecha.append(str(x.fecha))
                hora.append(str(x.hora))
                tipo.append(x.tipo)
                totalF.append(str(x.total_factura))
                id.append(x.id)
                totalC = totalC + x.total_factura
                fila = fila + 1
            fila = fila +1
            #formato para los valores
            format = workbook.add_format()
            format.set_align('center')
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 4, 15)
            worksheet.write_column('A3', id, format)
            worksheet.write_column('B3', fecha, format)
            worksheet.write_column('C3', hora, format)
            worksheet.write_column('D3', tipo, format)
            worksheet.write_column('E3', totalF, format)
            #worksheet.write('F2', str(totalC), format)
            worksheet.write('A'+str(fila), 'Total Facturado',formatT2)
            #formato para resultado total
            format = workbook.add_format()
            format.set_align('center')
            format.set_bg_color('silver')
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