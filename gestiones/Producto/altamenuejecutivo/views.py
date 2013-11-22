from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from boru.settings import PAGINADO_PRODUCTOS
from gestiones.Producto.altamenuejecutivo.forms import altaMenuEjecutivoForm
from gestiones.Producto.producto.models import Ejecutivo, Plato


@permission_required('Administrador.is_admin', login_url="login")
def altamenuejecutivo(request):

    platos_lista = Plato.objects.all().order_by('-activo')
    paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)
    platos = paginator.page(1)

    if request.method == 'POST':

        formulario = altaMenuEjecutivoForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha = formulario.cleaned_data['fecha_Inicio']
            fechaF = formulario.cleaned_data['fecha_fin']
            seccion = formulario.cleaned_data['seccion']
            menu = Ejecutivo.objects.create(nombre=nombre, precio=precio, stock=stock, descripcion=descripcion,
                                         fecha_Inicio=fecha, fecha_fin= fechaF, seccion=seccion)

            seccion.menuesE.add(menu)
            seccion.save()

            #recupero las ids de los platos que quiero agregar al menu
            lista_platos_seleccionado = request.POST.getlist('platos')
            #las recorro y rescato los platos y los asigno al menu
            for p in lista_platos_seleccionado:
                menu.platos.add(Plato.objects.get(pk=p))

            #guardo los cambios
            menu.save()
            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/altamenuejecutivo/altamenuejecutivoexito.html', {'formulario': formulario, 'plato': platos},
                                      context_instance=RequestContext(request))

        try:
            listaPlatos = []
            lista = request.session['listaProductosMenuEjecutivo']

            for p in lista:
                listaPlatos.append(Plato.objects.get(pk=p))
            platosLista = listaPlatos

            platos_selec = get_template('Producto/altamenuejecutivo/menuejecutivo_platos.html')
        except:
            platosLista=[]

        return render_to_response('Producto/altamenuejecutivo/altamenuejecutivo.html', {'formulario': formulario, 'plato': platos,'lista_platos':platos_selec.render(Context({'platos':platosLista}))},
                                  context_instance=RequestContext(request))

    else:
        try:
            request.session['listaProductosMenuEjecutivo']=[]
        except:
            pass

        formulario = altaMenuEjecutivoForm()
        return render_to_response('Producto/altamenuejecutivo/altamenuejecutivo.html', {'formulario': formulario, 'plato': platos},
                        context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        listado = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q)).order_by('-activo')[:30]

        return render_to_response('Producto/altamenuejecutivo/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarproductoajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']

        if q != "":
            platos = Plato.objects.filter( Q(nombre__icontains=q) | Q(seccion__nombre__icontains=q) ).order_by('-activo')
        else:
            platos_lista = Plato.objects.all().order_by("-activo")
            paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)
            platos = paginator.page(1)

        return render_to_response('Producto/altamenuejecutivo/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))



@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        platos_lista = Plato.objects.all().order_by('-activo')
        paginator = Paginator(platos_lista, PAGINADO_PRODUCTOS)

        try:
            platos = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            platos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            platos = paginator.page(paginator.num_pages)




        return render_to_response('Producto/altamenuejecutivo/busquedaresultados_items.html', {'plato': platos},
                                  context_instance=RequestContext(request))



@permission_required('Administrador.is_admin', login_url="login")
def agregarProductoListaAjax(request):

    platos = None

    if request.method == 'GET':

        id_prod = request.GET['id_prod']

        try:
            lista = request.session['listaProductosMenuEjecutivo']
        except:
            lista =[]

        if id_prod.isdigit():

            listaPlatos =[]

            try:
                lista.remove(id_prod)
            except:
                lista.append(id_prod)

            #lista.append(id_prod)
            request.session['listaProductosMenuEjecutivo']=lista

            for p in lista:
                listaPlatos.append(Plato.objects.get(pk=p))

            platos = listaPlatos

    return render_to_response('Producto/altamenuejecutivo/menuejecutivo_platos.html', {'platos': platos},
                              context_instance=RequestContext(request))