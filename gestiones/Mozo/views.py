from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Comanda.comanda.models import Comanda
from gestiones.Producto.producto.models import Bebida, Plato, DelDia, Ejecutivo
from gestiones.Salon.altamesa.models import Mesa
import datetime
from datetime import date
from time import time


@permission_required('Administrador.is_mozo', login_url="login")
def inicio(request):
    request.session['listaProductosComanda']=[]
    return render_to_response('Mozo/mozo.html', {}, context_instance=RequestContext(request))



@permission_required('Administrador.is_mozo', login_url="login")
def crearcomanda(request):

    #si se envio el formulario
    if request.method == 'POST':

        cantidad = request.POST['cantidadC']

        if cantidad.isdigit():

            request.session['cantidadC']=cantidad

            #recupero las mesas que estan activas
            mesas=Mesa.objects.filter(activo__exact=1)

            #recupero el panel que muestra las mesas seleccionadas
            panel_seleccionar_mesa=get_template('Mozo/panel_mesas_seleccionadas.html')

            #Creamos la comanda
            fecha = datetime.date.today()
            now = datetime.datetime.now()
            hora = datetime.time(now.hour, now.minute, now.second)
            comanda = Comanda.objects.create(fecha=fecha, hora=hora, cantidadC=cantidad)
            print(comanda.estrategia.nombre)

            #guardo en la sesion el id de la comanda
            request.session['id_comanda']= comanda.id

            #lo inserto en el resto del template y lo muestro
            return render_to_response('Mozo/seleccionar_mesas.html', {'panel_seleccionar_mesa':panel_seleccionar_mesa.render( Context({'cantidadC': cantidad}) ),'mesas':mesas }, context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse('mozo'))
    else:
        #si trato de entrar sin haber enviado el form,me vuelve a la primera pagina
        return HttpResponseRedirect(reverse('mozo'))

def seleccionarproductos(request):
    idcomanda = request.session["id_comanda"]
    print(idcomanda)
    comanda = Comanda.objects.get(pk=idcomanda)
    seccion = comanda.filtrar_secciones()

    try:
        pass#request.session['listaProductosComanda']=[]
    except:
        print("Excepcion en seleccionar productos")
    panel_seleccionar_producto=get_template('Mozo/panel_menu_seleccionado.html')
    return render_to_response('Mozo/seleccionar_menu.html', {'seccion': seccion, 'panel_seleccionar_mesa':panel_seleccionar_producto.render( Context({}) )}, context_instance=RequestContext(request))

def cargararproductosajax(request):
    print("Entre en la funcion de vista aca")
    if request.method == 'GET':
        id_seccion = request.GET['id_seccion']
        seccion = SeccionCarta.objects.get(pk=id_seccion)
        producto = seccion.dame_productos()
        return render_to_response('Mozo/productos_items.html', {'producto': producto}, context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def finalizar(request):
    return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))

@permission_required('Administrador.is_mozo', login_url="login")
def cargararmesasjax(request):
    print("aca llegue")
    if request.method == 'GET':
        id_mesa = request.GET['id_mesa']
        mesa = Mesa.objects.get(pk=id_mesa)
        print("pase")
        idcomanda =request.session["id_comanda"]
        print(idcomanda)
        comanda = Comanda.objects.get(pk=idcomanda)
        comanda.cargar_mesas(mesa)
        return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def sacarmesasjax(request):
    print("aca llegue para sacar")
    if request.method == 'GET':
        id_mesa = request.GET['id_mesa']
        mesa = Mesa.objects.get(pk=id_mesa)
        print("pase")
        idcomanda =request.session["id_comanda"]
        print(idcomanda)
        comanda = Comanda.objects.get(pk=idcomanda)
        comanda.sacar_mesas(mesa)
        return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))


@permission_required('Administrador.is_mozo', login_url="login")
def cancelarComandajax(request):
    print("Estoy por entrar para cancelar")
    #if request.method == 'GET':
    print("Entre lo que sigue es el id de cancelar")
    idcomanda =request.session["id_comanda"]
    comanda = Comanda.objects.get(pk=idcomanda)
    print(idcomanda)
    comanda.delete()
    return HttpResponseRedirect(reverse('mozo'))
    #comanda.remove()
    #return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))
    #return render_to_response('Mozo/finalizar_comanda.html', {}, context_instance=RequestContext(request))



@permission_required('Administrador.is_mozo', login_url="login")
def guardarproductosajax(request):
    print("voy a guardar")
    if request.method == 'GET':
        datos_producto = request.GET['datos_producto']
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

        return render_to_response('Mozo/panel_menu_seleccionado.html', {'producto': listaPlatos},
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