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
        #secciones = SeccionCarta.objects.filter(categoria= 'P')
        #self.fields['seccion'].widget = Select(choices=secciones)
        promocion = ((True, 'Si'), (False, 'No'))
        self.fields['enPromocion'].widget = Select(choices=promocion)

