from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Producto.altamenudia.forms import altaMenuDiaForm
from gestiones.Producto.producto.models import DelDia, Plato


@permission_required('Administrador.is_admin', login_url="login")
def altamenudia(request):

    """if request.method == 'POST' and request.POST['buscar'] == 'buscar':
        platos = Plato.objects.filter( Q(nombre__icontains=request.POST['q']) ).order_by('-activo')
    else:"""
    platos = Plato.objects.all().order_by('-activo')[:8]

    if request.method == 'POST':
        formulario = altaMenuDiaForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha = formulario.cleaned_data['fecha_Inicio']
            menu = DelDia.objects.create(nombre=nombre,precio= precio,stock= stock, descripcion=descripcion,fecha_Inicio= fecha)

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/altamenudia/altamenudiaexito.html', {'formulario': formulario, 'plato': platos},
                                      context_instance=RequestContext(request))

        return render_to_response('Producto/altamenudia/altamenudia.html', {'formulario': formulario, 'plato': platos},
                                  context_instance=RequestContext(request))

    else:

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
