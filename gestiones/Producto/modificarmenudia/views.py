from _ast import unaryop
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from boru.settings import PAGINADO_PRODUCTOS
from gestiones.Producto.modificarmenudia.forms import modificarMenuDiaForm
from gestiones.Producto.producto.models import DelDia, Plato
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


@permission_required('Administrador.is_admin', login_url="login")
def modificarmenudia(request, id_menu=None):

    #rescato los platos
    platos_lista = Plato.objects.all().order_by('nombre')
    paginator = Paginator(platos_lista, 4)
    platos = paginator.page(1)

    #rescato los menues
    menues = DelDia.objects.all().order_by('nombre')

    try:
        #obtengo en el caso de que venga el id por GET, al menu
        unMenu = DelDia.objects.get(pk=id_menu)

        #creo diccionario con los datos del menu para mostrarlos ne el formulario
        datosMenu = {'id': unMenu.id, 'nombre': unMenu.nombre, 'precio': unMenu.precio, 'stock': unMenu.stock,
                     'descripcion': unMenu.descripcion,'fecha_Inicio': unMenu.fecha_Inicio
                    ,'seccion': unMenu.seccion, 'activo': unMenu.activo, 'platos': unMenu.platos}

    except:
        datosMenu = ''
        unMenu = None


        #si se apreto el boton de modificar
    if request.method == 'POST' and unMenu != None:

        #le indico al form que tome los datos del request y le paso la instancia del menu  que obtuve mas arriba
        formulario = modificarMenuDiaForm(request.POST, instance=unMenu)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha_Inicio = formulario.cleaned_data['fecha_Inicio']
            seccion = formulario.cleaned_data['seccion']
            activo = formulario.cleaned_data['activo']
            #platos = formulario.cleaned_data['platos']


            #seteo los nuevos datos en el objeto unMenu que obtuvimos al principio
            unMenu.nombre = nombre
            unMenu.precio = precio
            unMenu.stock = stock
            unMenu.descripcion = descripcion
            unMenu.fecha_Inicio = fecha_Inicio
            unMenu.seccion = seccion
            unMenu.activo = activo
           #     unMenu.platos = platos
            unMenu.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/modificarmenudia/modificarmenudiaExito.html',
                                      {'formulario': formulario, 'menues': menues},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Producto/modificarmenudia/modificarmenudia.html',
                                  {'formulario': formulario, 'menues': menues, 'plato':platos},
                                  context_instance=RequestContext(request))

    else:
        #si no apretamos el boton modificar menu y seleccionamos algun menu, mostramos sus datos, sino mostramos el form vacio
        formulario = modificarMenuDiaForm(initial=datosMenu)
        platos_selec = get_template('Producto/modificarmenudia/menudia_platos.html')

        try:
            listaPlatos = []
            #lista = request.session['listaProductosModificarMenuDia']

            for p in unMenu.platos.all():

                listaPlatos.append(Plato.objects.get(pk=p.id))
                #request.session['listaProductosModificarMenuDia'].append(p.id)

            platosLista = listaPlatos
            #request.session['listaProductosModificarMenuDia'] = lista

        except:
            platosLista = []

        return render_to_response('Producto/modificarmenudia/modificarmenudia.html',
                                  {'formulario': formulario, 'menues': menues, 'plato':platos,
                                   'lista_platos': platos_selec.render(Context({'platos': platosLista}))
                                  },
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarmenudel(request, id_menu):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unMenu = DelDia.objects.get(pk=id_menu)
    except:
        unMenu = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unMenu != None:

        if unMenu.activo:
            unMenu.activo = False
        else:
            unMenu.activo = True

        unMenu.save()

    return HttpResponseRedirect(reverse('modificarmenudia'))





@permission_required('Administrador.is_admin', login_url="login")
def agregarProductoListaAjax(request):

    platos = None

    if request.method == 'GET':

        id_prod = request.GET['id_prod']

        try:
            lista = request.session['listaProductosModificarMenuDia']
        except:
            lista =[]

        if id_prod.isdigit():

            listaPlatos =[]

            try:
                lista.remove(id_prod)
            except:
                lista.append(id_prod)

            #lista.append(id_prod)
            request.session['listaProductosModificarMenuDia']=lista

            for p in lista:
                listaPlatos.append(Plato.objects.get(pk=p))

            platos = listaPlatos

    return render_to_response('Producto/modificarmenudia/menudia_platos.html', {'platos': platos},
                              context_instance=RequestContext(request))