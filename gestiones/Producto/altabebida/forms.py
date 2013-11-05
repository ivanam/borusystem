from django.forms import ModelForm, Select
from gestiones.Producto.producto.models import Bebida


class altaBebidaForm(ModelForm):
    class Meta:
        model = Bebida
        fields = (
            'nombre', 'marca', 'precio', 'descuento', 'stock', 'enPromocion', 'activo')


    def __init__(self, *args, **kwargs):
        super(altaBebidaForm, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo


        #formateando los inputs
        ACTIVO = ((True, 'Activo'), (False, 'Inactivo'))
        self.fields['activo'].widget = Select(choices=ACTIVO)
        EN_PROMOCION = ((True, 'Si'), (False, 'No'))
        self.fields['enPromocion'].widget = Select(choices=EN_PROMOCION)