from django.forms import ModelForm, Select
from gestiones.Producto.producto.models import Bebida


class modificarBebida(ModelForm):
    class Meta:
        model = Bebida
        fields = (
            'nombre', 'precio', 'stock', 'activo', 'marca', 'enPromocion', 'descuento', 'seccion')


    def __init__(self, *args, **kwargs):
        super(modificarBebida, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo

        #formateando los inputs
        ACTIVO = ((True, 'Activo'), (False, 'Inactivo'))
        self.fields['activo'].widget = Select(choices=ACTIVO)
        EN_PROMOCION = ((True, 'Si'), (False, 'No'))
        self.fields['enPromocion'].widget = Select(choices=EN_PROMOCION)