from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Producto.altamenudia.forms import altaMenuDiaForm
from gestiones.Producto.producto.models import DelDia, Plato


@permission_required('Administrador.is_admin', login_url="login")
def altamenudia(request):
    platos = Plato.objects.all#all.order_by('-is_active')

    if request.method == 'POST':
        formulario = altaMenuDiaForm(request.POST)

        if formulario.is_valid():
            #capturamos y limpiamos datos
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            descripcion = formulario.cleaned_data['descripcion']
            fecha = formulario.cleaned_data['fecha_Inicio']
            menu = DelDia(nombre, precio, stock, descripcion, fecha)
            menu.save()


    formulario = altaMenuDiaForm()
    return render_to_response('Producto/altamenudia/altamenudia.html', {'formulario': formulario, 'Plato': platos},
                              context_instance=RequestContext(request))

