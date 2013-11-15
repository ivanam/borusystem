from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from gestiones.Producto.altamenudia.forms import altaMenuDiaForm
from gestiones.Producto.producto.models import DelDia, Plato


@permission_required('Administrador.is_admin', login_url="login")
def altamenudia(request):

    platos = Plato.objects.all().order_by('-activo')[:30]

    if request.method == 'POST':
        formulario = altaMenuDiaForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha = formulario.cleaned_data['fecha_Inicio']
            seccion = formulario.cleaned_data['seccion']
            menu = DelDia.objects.create(nombre=nombre, precio=precio, stock=stock, descripcion=descripcion,
                                         fecha_Inicio=fecha, seccion=seccion)

            seccion.menuesD.add(menu)
            seccion.save()

            #recupero las ids de los platos que quiero agregar al menu
            lista_platos_seleccionado = request.POST.getlist('chkId')
            #las recorro y rescato los platos y los asigno al menu
            for p in lista_platos_seleccionado:
                menu.platos.add(Plato.objects.get(pk=p))

            #guardo los cambios
            menu.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/altamenudia/altamenudiaexito.html', {'formulario': formulario, 'plato': platos},
                                      context_instance=RequestContext(request))

        try:
            listaPlatos = []
            lista = request.session['listaProductosMenuDia']

            for p in lista:
                listaPlatos.append(Plato.objects.get(pk=p))
            platosLista = listaPlatos

            platos_selec = get_template('Producto/altamenudia/menudia_platos.html')
        except:
            platosLista=[]

        return render_to_response('Producto/altamenudia/altamenudia.html', {'formulario': formulario, 'plato': platos,'lista_platos':platos_selec.render(Context({'platos':platosLista}))},
                                  context_instance=RequestContext(request))

    else:
        try:
            request.session['listaProductosMenuDia']=[]
        except:
            pass

        formulario = altaMenuDiaForm()
        return render_to_response('Producto/altamenudia/altamenudia.html', {'formulario': formulario, 'plato': platos},
                        context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = Plato.objects.filter( Q(nombre__icontains=q) ).order_by('-activo')[:30]

        return render_to_response('Producto/altamenudia/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']
        platos = Plato.objects.filter( Q(nombre__icontains=q) ).order_by('-activo')

        return render_to_response('Producto/altamenudia/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def agregarProductoListaAjax(request):

    platos = None

    if request.method == 'GET':

        id_prod = request.GET['id_prod']

        try:
            lista = request.session['listaProductosMenuDia']
        except:
            lista =[]

        if id_prod.isdigit():

            listaPlatos =[]

            try:
                lista.remove(id_prod)
            except:
                pass

            lista.append(id_prod)
            request.session['listaProductosMenuDia']=lista

            for p in lista:
                listaPlatos.append(Plato.objects.get(pk=p))

            platos = listaPlatos

    return render_to_response('Producto/altamenudia/menudia_platos.html', {'platos': platos},
                              context_instance=RequestContext(request))