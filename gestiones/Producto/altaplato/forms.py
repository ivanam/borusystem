from django.forms import ModelForm
from django.forms.widgets import Select
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Plato


class altaPlatoForm(ModelForm):
    class Meta:
        model = Plato
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'enPromocion', 'descuento', 'seccion')


    def __init__(self, *args, **kwargs):
        super(altaPlatoForm, self).__init__(*args, **kwargs)

        #selecciono las secciones de la carta que son solo de platos
        seccionesChoice = SeccionCarta.objects.filter(categoria= 'P')
        #las formateo para crear un choice
        secciones = [(secc.id, secc.nombre) for secc in seccionesChoice]
        #indico que el widget tiene que mostrar el choice recien creado
        self.fields['seccion'].widget = Select(choices=secciones)
        promocion = ((True, 'Si'), (False, 'No'))
        self.fields['enPromocion'].widget = Select(choices=promocion)
