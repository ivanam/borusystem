from decimal import Decimal
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from boru.settings import PAGINADO_PRODUCTOS, STATIC_URL
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Comanda.comanda.models import Comanda, DetalleComanda
from gestiones.Producto.producto.models import Bebida, Plato, DelDia, Ejecutivo, MenuS
from gestiones.Salon.altamesa.models import Mesa
import datetime


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    request.session['listaProductosComanda']=[]
    request.session['listaMesasComanda']=[]
    request.session['total'] = 0
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






#------------------------------------------Inicio de Mis comandas--------------------------------------------------------


@permission_required('Administrador.is_mozo', login_url="login")
def miscomandas(request,pagina=1):

    if pagina == None:
        pagina = 1

    comandas_lista = Comanda.objects.filter(tipo_comanda__exact="C", finalizada = True, cerrada = False).order_by("-fecha", "-hora")
    paginator = Paginator(comandas_lista, PAGINADO_PRODUCTOS)
    comandas = paginator.page(pagina)

    #abro el modelo de comanda abierta
    detalle_comanda=get_template('Mozo/item_comanda_abierta.html')
    #renderizo el template html
    detalle_renderizado=detalle_comanda.render(Context({'comandas': comandas,'STATIC_URL':STATIC_URL}))

    print(detalle_renderizado)
    return render_to_response('Mozo/mis_comandas.html', {"item_comandas_abiertas": detalle_renderizado,"titulo":"Comandas Abiertas"}, context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def polling_comandas(request):
    if request.method == "GET":
        print("Aca entre")
        comandas_nuevas=Comanda.objects.filter(tipo_comanda__exact="C",vista=False,finalizada=True,cerrada=False).count()
        pedidos_nuevos =Comanda.objects.filter(tipo_comanda__exact="P",vista=False,finalizada=True,cerrada=True).count()

    return render_to_response('Mozo/comandas_nuevas.html',{'numero':comandas_nuevas,'numero_pedido':pedidos_nuevos},context_instance=RequestContext(request))


