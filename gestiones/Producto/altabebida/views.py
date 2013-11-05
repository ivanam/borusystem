from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Producto.altabebida.forms import altaBebidaForm
from gestiones.Producto.producto.models import Bebida


@permission_required('Administrador.is_admin', login_url="login")
def altabebida(request):
    if request.method == 'POST':

        formulario = altaBebidaForm(request.POST)

        if formulario.is_valid():

            #capturamos y limpiamos datos
            nombre = formulario.cleaned_data['nombre']
            precio = formulario.cleaned_data['precio']
            stock = formulario.cleaned_data['stock']
            activo = formulario.cleaned_data['activo']
            enPromocion = formulario.cleaned_data['enPromocion']
            marca = formulario.cleaned_data['marca']
            descuento = formulario.cleaned_data['descuento']

            bebida = Bebida.objects.create(nombre=nombre, precio=precio, stock=stock, activo=activo,
                                           enPromocion=enPromocion, marca=marca, descuento=descuento)

            #mostramos que la operacion fue exitosa
            return render_to_response('Producto/altabebida/altabebidaexito.html', {},
                                      context_instance=RequestContext(request))

        return render_to_response('Producto/altabebida/altabebida.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

    else:

        formulario = altaBebidaForm()
        return render_to_response('Producto/altabebida/altabebida.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))