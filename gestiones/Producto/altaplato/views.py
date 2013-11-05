from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gestiones.Producto.altaplato.forms import altaPlatoForm
from gestiones.Producto.producto.models import Plato


@permission_required('Administrador.is_admin', login_url="login")
def altaplato(request):
    if request.method == 'POST':
        formulario=altaPlatoForm(request.POST)
        if formulario.is_valid():
                nombre = formulario.cleaned_data['nombre']
                precio = formulario.cleaned_data['precio']
                stock = formulario.cleaned_data['stock']
                descripcion = formulario.cleaned_data['descripcion']
                promocion = formulario.cleaned_data['enPromocion']
                descuento = formulario.cleaned_data['descuento']
                seccion = formulario.cleaned_data['seccion']
                if seccion.categoria == 'P':
                    plato = Plato.objects.create(nombre=nombre, precio=precio,stock=stock, descripcion=descripcion, enPromocion=promocion, descuento=descuento, seccion=seccion)
                    seccion.platoss.add(plato)
                    seccion.save()
                    return render_to_response('Producto/altaplato/altaplatoexito.html', {},context_instance=RequestContext(request))
                else:
                    return render_to_response('Producto/altaplato/altaplatoerror.html', {},context_instance=RequestContext(request))
        else:
            return render_to_response('Producto/altaplato/altaplato.html', {'formulario': formulario},context_instance=RequestContext(request))
    else:
        formulario=altaPlatoForm()
        return render_to_response('Producto/altaplato/altaplato.html', {'formulario': formulario},context_instance=RequestContext(request))


