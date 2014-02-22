from decimal import Decimal
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from boru.settings import PAGINADO_PRODUCTOS, STATIC_URL
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Comanda.comanda.models import Comanda, DetalleComanda, Preticket, Factura
from gestiones.Producto.producto.models import Bebida, Plato, DelDia, Ejecutivo, MenuS
from gestiones.Salon.altamesa.models import Mesa
import datetime


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    request.session['listaProductosComanda']=[]
    request.session['listaMesasComanda']=[]
    request.session['total'] = 0
    request.session['id_comanda'] = 0
    return render_to_response('Mozo/mozo.html', {"crear_comanda":True}, context_instance=RequestContext(request))



@permission_required('Administrador.is_mozo', login_url="login")
def crearcomanda(request):

    #si se envio el formulario
    if request.method == 'POST':

        cantidad = request.POST['cantidadC']

        if (cantidad.isdigit()) and (int(cantidad)>0):

            request.session['cantidadC']=cantidad
            request.session['total'] = 0

            #recupero las mesas que estan activas
            mesas=Mesa.objects.filter(activo__exact=1).order_by("sector")
            #recupero el panel que muestra las mesas seleccionadas
            panel_seleccionar_mesa=get_template('Mozo/panel_mesas_seleccionadas.html')
            if request.session['id_comanda'] == 0:
                #Creamos la comanda
                fecha = datetime.date.today()
                now = datetime.datetime.now()
                hora = datetime.time(now.hour, now.minute, now.second)
                comanda = Comanda.objects.create(fecha=fecha, hora=hora, cantidadC=cantidad)
                comanda.mozo = request.user
                comanda.finalizada = False
                comanda.save()
                #guardo en la sesion el id de la comanda
                request.session['id_comanda']= comanda.id
            else:
                mesas_seleccionadas = request.session['listaMesasComanda']
                for id_mesa in mesas_seleccionadas:
                    mesa = Mesa.objects.get(pk=id_mesa)
                    mesa.ocupada = False
                    mesa.save()
                request.session['listaMesasComanda'] = []

            #lo inserto en el resto del template y lo muestro
            return render_to_response('Mozo/seleccionar_mesas.html', {"seleccionar_mesa":True, 'panel_seleccionar_mesa':panel_seleccionar_mesa.render( Context({'cantidadC': cantidad}) ),'mesas':mesas }, context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse('mozo'))
    else:
        #si trato de entrar sin haber enviado el form,me vuelve a la primera pagina
        return HttpResponseRedirect(reverse('mozo'))


@permission_required('Administrador.is_mozo', login_url="login")
def vistaMesas(request):
    cantidad = request.session['cantidadC']
    mesas_seleccionadas = request.session['listaMesasComanda']
    for id_mesa in mesas_seleccionadas:
        mesa = Mesa.objects.get(pk=id_mesa)
        mesa.ocupada = False
        mesa.save()
    mesas_seleccionadas = []
    request.session['listaMesasComanda']= mesas_seleccionadas
    mesas=Mesa.objects.filter(activo__exact=1).order_by("sector")
    panel_seleccionar_mesa=get_template('Mozo/panel_mesas_seleccionadas.html')
    return render_to_response('Mozo/seleccionar_mesas.html', {'panel_seleccionar_mesa':panel_seleccionar_mesa.render( Context({'cantidadC': cantidad}) ),'mesas':mesas }, context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def seleccionarproductos(request):
    idcomanda = request.session["id_comanda"]
    comanda = Comanda.objects.get(pk=idcomanda)
    seccion = comanda.filtrar_secciones()
    total = request.session["total"]
    #TODO mi no enteder esto
    try:
        pass
    except:
        print("Excepcion en seleccionar productos")

    lista = request.session['listaProductosComanda']
    listaPlatos = []
    for producto in lista:
            print(producto)
            datos = producto.split('_')
            id_prod = datos[0]
            cantidad = datos[1]
            categoria = datos[2]
            print(id_prod)
            print (cantidad)
            print(categoria)
            if categoria == 'P':
                listaPlatos.append(Plato.objects.get(pk=id_prod))
            if categoria == 'B':
                listaPlatos.append(Bebida.objects.get(pk=id_prod))
            if categoria == 'D':
                listaPlatos.append(DelDia.objects.get(pk=id_prod))
            if categoria == 'E':
                listaPlatos.append(Ejecutivo.objects.get(pk=id_prod))
    panel_seleccionar_producto=get_template('Mozo/panel_menu_seleccionado.html')
    return render_to_response('Mozo/seleccionar_menu.html', {"seleccionar_menu":True,'seccion': seccion, 'panel_seleccionar_mesa':panel_seleccionar_producto.render( Context({'producto': listaPlatos, 'total':total}) )}, context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def cargararproductosajax(request):
    print("Entre en la funcion de vista aca")
    if request.method == 'GET':
        id_seccion = request.GET['id_seccion']
        seccion = SeccionCarta.objects.get(pk=id_seccion)
        producto = seccion.dame_productos()
        return render_to_response('Mozo/productos_items.html', {'producto': producto}, context_instance=RequestContext(request))

#@permission_required('Administrador.is_mozo', login_url="login")
#def finalizar(request):
 #   return render_to_response('Mozo/fidanalizar_comanda.html', {}, context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def cargararmesasjax(request):
    print("aca llegue")
    if request.method == 'GET':
        id_mesa = request.GET['id_mesa']
        lista = request.session["listaMesasComanda"]
        lista.append(id_mesa)
        request.session["listaMesasComanda"] = lista
        mesa = Mesa.objects.get(pk=id_mesa)
        mesa.ocupada = True
        mesa.save()
        print("pase")
        idcomanda =request.session["id_comanda"]
        print(idcomanda)
        #comanda = Comanda.objects.get(pk=idcomanda)
        #comanda.cargar_mesas(mesa)
        return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def sacarmesasjax(request):
    print("aca llegue para sacar")
    if request.method == 'GET':
        id_mesa = request.GET['id_mesa']
        lista = request.session["listaMesasComanda"]
        ubicacion = lista.index(id_mesa)
        del lista[ubicacion]
        request.session["listaMesasComanda"] = lista
        mesa = Mesa.objects.get(pk=id_mesa)
        mesa.ocupada= False
        mesa.save()
        print("pase")
        idcomanda =request.session["id_comanda"]
        print(idcomanda)
        #comanda = Comanda.objects.get(pk=idcomanda)
        #comanda.sacar_mesas(mesa)
        return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def cancelarComandajax(request):
    print("Estoy por entrar para cancelar")
    #if request.method == 'GET':
    print("Entre lo que sigue es el id de cancelar")
    idcomanda =request.session["id_comanda"]
    comanda = Comanda.objects.get(pk=idcomanda)
    print(idcomanda)
    mesas_seleccionadas = request.session['listaMesasComanda']
    productos_seleccionados = request.session['listaProductosComanda']
    for id_mesa in mesas_seleccionadas:
        mesa = Mesa.objects.get(pk=id_mesa)
        mesa.ocupada = False
        mesa.save()
    for producto in productos_seleccionados:
        datos = producto.split('_')
        id_prod = datos[0]
        cantidad = datos[1]
        categoria = datos[2]
        if categoria == 'P':
             prod = Plato.objects.get(pk=id_prod)
        if categoria == 'B':
              prod = Bebida.objects.get(pk=id_prod)
        if categoria == 'D':
            prod = DelDia.objects.get(pk=id_prod)
        if categoria == 'E':
            prod = Ejecutivo.objects.get(pk=id_prod)
        prod.stock = prod.stock + Decimal(cantidad)
        prod.save()
    comanda.delete()
    request.session['listaProductosComanda']=[]
    request.session['listaMesasComanda']=[]
    #return render_to_response('Mozo/mozo.html', {}, context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('mozo'))
    #comanda.remove()
    #return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))
    #return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))



@permission_required('Administrador.is_mozo', login_url="login")
def guardarproductosajax(request):
    print("voy a guardar")
    if request.method == 'GET':
        datos_producto = request.GET['datos_producto']
        datosp = datos_producto.split('_')
        id = datosp[0]
        cantidadp = datosp[1]
        cat = datosp[2]
        if cat=='P':
            prod = Plato.objects.get(pk=id)
        if cat=='B':
            prod = Bebida.objects.get(pk=id)
        if cat=='D':
            prod = DelDia.objects.get(pk=id)
        if cat=='E':
            prod = Ejecutivo.objects.get(pk=id)
        prod.stock = prod.stock - Decimal (cantidadp)
        prod.save()
        subtotal = prod.importe() * Decimal(cantidadp)
        total = request.session['total']+ subtotal
        request.session['total']= total
        #producto = Bebida.objects.get(pk=id_prod)
        print("pase a guardar")
        lista = request.session['listaProductosComanda']
        lista.append(datos_producto)
        request.session['listaProductosComanda'] = lista
        #print (lista)
        listaPlatos = []
        for producto in lista:
            print(producto)
            datos = producto.split('_')
            id_prod = datos[0]
            cantidad = datos[1]
            categoria = datos[2]
            print(id_prod)
            print (cantidad)
            print(categoria)
            if categoria == 'P':
                listaPlatos.append(Plato.objects.get(pk=id_prod))
            if categoria == 'B':
                listaPlatos.append(Bebida.objects.get(pk=id_prod))
            if categoria == 'D':
                listaPlatos.append(DelDia.objects.get(pk=id_prod))
            if categoria == 'E':
                listaPlatos.append(Ejecutivo.objects.get(pk=id_prod))

        return render_to_response('Mozo/panel_menu_seleccionado.html', {'producto': listaPlatos, 'total':total},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def cargarpanelajax(request):
    print("voy a cargar el panel")
    lista = request.session['listaProductosComanda']
    listaPlatos = []
    for producto in lista:
        listaPlatos.append(Bebida.objects.get(pk=producto))
    return render_to_response('Mozo/panel_menu_seleccionado.html', {'producto': listaPlatos},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def finalizar(request):
    print("voy a mostrar el final de la comanda")
    lista = request.session['listaProductosComanda']
    cantidadComensales = request.session['cantidadC']
    total = request.session['total']
    #id_comanda = request.session["id_comanda"]
    #comanda = Comanda.objects.get(pk=id_comanda)

    #mesas = ""
    #listam = request.session['listaMesasComanda']
    #for mesa in listam:
    #    mesas = mesas+str(mesa)+", "

    menuS = []
    for producto in lista:
            print(producto)
            datos = producto.split('_')
            id_prod = datos[0]
            cantidad = datos[1]
            categoria = datos[2]
            print(id_prod)
            print (cantidad)
            print(categoria)
            if categoria == 'P':
                plato = Plato.objects.get(pk=id_prod)
                men = MenuS(plato.nombre, cantidad, plato.importe())
                menuS.append(men)
            if categoria == 'B':
                bebida = Bebida.objects.get(pk=id_prod)
                men = MenuS(bebida.nombre, cantidad, bebida.importe())
                menuS.append(men)
            if categoria == 'D':
                deldia = DelDia.objects.get(pk=id_prod)
                men = MenuS(deldia.nombre, cantidad, deldia.precio)
                menuS.append(men)
            if categoria == 'E':
                ejecutivo = Ejecutivo.objects.get(pk=id_prod)
                men = MenuS(ejecutivo.nombre, cantidad, ejecutivo.precio)
                menuS.append(men)

    return render_to_response('Mozo/finalizar_comanda.html', {"finalizar":True,'cantidad': cantidadComensales, 'mesas': request.session['listaMesasComanda'], 'menuS':menuS, 'total':total},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def guardarComanda(request):
    print("voy a guardar la comanda")
    lista = request.session['listaProductosComanda']
    cantidadComensales = request.session['cantidadC']
    mesas = request.session['listaMesasComanda']
    idcomanda = request.session["id_comanda"]
    comanda = Comanda.objects.get(pk=idcomanda)
    comanda.cantidadC = cantidadComensales
    for id_mesa in mesas:
        mesa = Mesa.objects.get(pk=id_mesa)
        comanda.mesas.add(mesa)
        comanda.save()
    #TODO no usamos la estrategia para cargar productos:def cargarProductos(self, comanda, producto, cantidad)
    for producto in lista:
            print(producto)
            datos = producto.split('_')
            id_prod = datos[0]
            cantidad = datos[1]
            categoria = datos[2]
            if categoria == 'P':
                plato = Plato.objects.get(pk=id_prod)
                detalle = DetalleComanda.objects.create(nombre=plato.nombre,cantidadP=cantidad, platos= plato, precioXunidad=plato.importe(),descuento=plato.descuento)
            if categoria == 'B':
                bebida = Bebida.objects.get(pk=id_prod)
                detalle = DetalleComanda.objects.create(nombre=bebida.nombre,cantidadP=cantidad, bebidas= bebida , precioXunidad=bebida.importe(),descuento=bebida.descuento)
            if categoria == 'D':
                dia = DelDia.objects.get(pk=id_prod)
                detalle = DetalleComanda.objects.create(nombre=dia.nombre,cantidadP=cantidad, menuD= dia, precioXunidad=dia.precio,descuento=0)
            if categoria == 'E':
                ejecutivo = Ejecutivo.objects.get(pk=id_prod)
                detalle = DetalleComanda.objects.create(nombre=ejecutivo.nombre,cantidadP=cantidad, menuE= ejecutivo, precioXunidad=ejecutivo.precio,descuento=0)
            comanda.detalles.add(detalle)
            comanda.save()
    comanda.finalizar()
    return HttpResponseRedirect(reverse('mozo'))

@permission_required('Administrador.is_mozo', login_url="login")
def eliminarProductosAjaxSeleccionado(request):
    id_prod = request.GET['id']
    lista = request.session['listaProductosComanda']
    for producto in lista:
        datos = producto.split('_')
        id = datos[0]
        cantidad = datos[1]
        categoria = datos[2]
        if (id == id_prod):
            ubicacion = lista.index(producto)
            del lista[ubicacion]
            if categoria == 'P':
                prod = (Plato.objects.get(pk=id))
            if categoria == 'B':
                prod = (Bebida.objects.get(pk=id))
            if categoria == 'D':
                prod = (DelDia.objects.get(pk=id))
            if categoria == 'E':
                prod = (Ejecutivo.objects.get(pk=id))

            prod.stock = prod.stock + Decimal(cantidad)
            prod.save()
            subtotal = prod.importe() * Decimal(cantidad)
            total = request.session['total'] - subtotal
            request.session['total']= total
            request.session['listaProductosComanda'] = lista
            print ("producto eliminado con exito")
            break

    listaPlatos = []
    for producto in lista:
        print(producto)
        datos = producto.split('_')
        id_prod = datos[0]
        categoria = datos[2]
        if categoria == 'P':
            listaPlatos.append(Plato.objects.get(pk=id_prod))
        if categoria == 'B':
            listaPlatos.append(Bebida.objects.get(pk=id_prod))
        if categoria == 'D':
            listaPlatos.append(DelDia.objects.get(pk=id_prod))
        if categoria == 'E':
            listaPlatos.append(Ejecutivo.objects.get(pk=id_prod))


    return render_to_response('Mozo/panel_menu_seleccionado.html', {'producto': listaPlatos, 'total':total},
                              context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def miscomandas(request,pagina=1):

    if pagina == None:
        pagina = 1

    #calculo fecha para filtrar las comandas y dejar las de hoy y ayer nomas
    hoy = datetime.date.today()
    ayer = datetime.date.today() - datetime.timedelta(days=1)

    titulo = "Mis Comandas del " + str(ayer.strftime("%d-%m-%Y")) + " y " + str(hoy.strftime("%d-%m-%Y"))

    comandas_lista = Comanda.objects.filter(fecha__range=(ayer, hoy),mozo__id=request.user.id).order_by("-fecha", "-hora")
    paginator = Paginator(comandas_lista, PAGINADO_PRODUCTOS)
    comandas = paginator.page(pagina)

    #abro el modelo de comanda abierta
    detalle_comanda = get_template('Mozo/item_comanda_abierta.html')
    #renderizo el template html
    detalle_renderizado = detalle_comanda.render(Context({'listado': comandas, 'STATIC_URL': STATIC_URL}))

    return render_to_response('Mozo/miscomandas.html',{'listado_comandas':detalle_renderizado,'miscomandas':True,"titulo": titulo},context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def detalle_comanda_ajax(request):
    if request.method == "GET":
        id_comanda = request.GET["id_comanda"]
        comanda = Comanda.objects.get(pk=id_comanda)
        total = comanda.total()

        return render_to_response('Cajero/detalle_comanda.html', {'comanda': comanda,'total':total},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def detalle_preticket_ajax(request):
    if request.method == "GET":
        id_preticket = request.GET["id_preticket"]
        preticket = Preticket.objects.get(pk=id_preticket)
        total = preticket.total_preticket

        return render_to_response('Cajero/detalle_preticket.html', {'preticket': preticket,'total':total},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def editar_detalle_comanda_ajax(request):
    if request.method == "GET":
        id_comanda = request.GET["id_comanda"]
        comanda = Comanda.objects.get(pk=id_comanda)
        total = comanda.total()

        return render_to_response('Mozo/editar_detalle_comanda.html', {'comanda': comanda,'total':total},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def detalle_factura_ajax(request):
    if request.method == "GET":
        id_factura = request.GET["id_factura"]
        factura = Factura.objects.get(pk=id_factura)
        total = factura.total_factura
        print(factura.total_factura)
        return render_to_response('Cajero/detalle_factura.html', {'factura': factura,'total':total},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def cerrar_comanda(request, id_comanda=None):

    comanda = Comanda.objects.get(pk=id_comanda)
    comanda.cerrada = True
    comanda.save()
    generar_preticket(request,id_comanda)
    return HttpResponseRedirect(reverse('una_comanda_mozo',args=[id_comanda]))



@permission_required('Administrador.is_mozo', login_url="login")
def generar_preticket(request,id_comanda=None):

    comanda = Comanda.objects.get(pk=id_comanda)
    comanda.estrategia.generar_preticket(comanda)

    return HttpResponseRedirect(reverse('una_comanda_mozo', args=[id_comanda]))


@permission_required('Administrador.is_mozo', login_url="login")
def guardar_detalle_comanda_ajax(request):
    if request.method == "POST":

        #recupero las ids de los platos que quiero agregar al menu
        lista_productos = request.POST.getlist('producto')
        comanda_id = request.POST.get('comanda_id')

        try:
            #obtengo la Comanda
            comanda = Comanda.objects.get(pk=comanda_id)

            #solo si la lista no esta vacia la limpio para volver a agregar los productos
            if lista_productos != []:
                comanda.limpiarDetalles(True)

            #las recorro y rescato los platos y los asigno al menu
            for p in lista_productos:

                cad = p.split("_")
                id_prod = cad[0]
                categoria = cad[1]
                cantidad = cad[2]

                if categoria == "P":
                    productoNuevo = Plato.objects.get(pk=id_prod)
                    print "es plato " + productoNuevo.nombre
                else:
                    if categoria == "B":
                        productoNuevo = Bebida.objects.get(pk=id_prod)
                        print "es bebida " + productoNuevo.nombre
                    else:
                        if categoria == "D":
                            productoNuevo = DelDia.objects.get(pk=id_prod)
                            print "es deldia " + productoNuevo.nombre
                        else:
                            productoNuevo = Ejecutivo.objects.get(pk=id_prod)
                            print "es es ejecutivo " + productoNuevo.nombre

                comanda.agregarDetalle(productoNuevo, cantidad)

        except:
            print "Error, no se pudo agregar el producto a la Comanda!"

    return HttpResponseRedirect(reverse('una_comanda_mozo', args=[comanda.pk]))


@permission_required('Administrador.is_mozo', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']

        resultados=[]

        platos = Plato.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        bebidas = Bebida.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        delDia = DelDia.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        ejecutivo = Ejecutivo.objects.filter(Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by(
            'nombre').filter(activo=True)

        resultados.extend(platos)
        resultados.extend(bebidas)
        resultados.extend(delDia)
        resultados.extend(ejecutivo)

        return render_to_response('Mozo/busquedaresultados.html', {'listado': resultados},
                                  context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        resultados = []

        if q != "":
            platos = Plato.objects.filter( Q(nombre__iexact=q) | Q(seccion__nombre__iexact=q) ).order_by('nombre').filter(activo = True)

            bebidas = Bebida.objects.filter( Q(nombre__iexact=q) | Q(seccion__nombre__iexact=q) ).order_by('nombre').filter(activo = True)

            delDia = DelDia.objects.filter( Q(nombre__iexact=q) | Q(seccion__nombre__iexact=q) ).order_by('nombre').filter(activo = True)

            ejecutivo = Ejecutivo.objects.filter( Q(nombre__iexact=q) | Q(seccion__nombre__iexact=q) ).order_by('nombre').filter(activo = True)

            resultados.extend(platos)
            resultados.extend(bebidas)
            resultados.extend(delDia)
            resultados.extend(ejecutivo)


        return render_to_response('Mozo/busquedaresultados_items.html', {'plato': resultados},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def una_comanda(request, id_comanda=None):
    try:
        lista_comandas = []
        lista_comandas.append( Comanda.objects.get(pk=id_comanda))
        detalle_generico = get_template('Mozo/item_comanda_abierta.html')
        return render_to_response('Mozo/miscomandas.html',
                                  {"una_comanda": detalle_generico.render(Context({'listado': lista_comandas,'STATIC_URL':STATIC_URL})),
                                   "titulo": "Comanda Seleccionada", 'miscomandas': True},
                                  context_instance=RequestContext(request))

    except Exception:
        return HttpResponse("Error, la comanda no fue encontreda en el Systema")
