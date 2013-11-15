from django.forms import ModelForm, Select
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Bebida


class altaBebidaForm(ModelForm):
    class Meta:
        model = Bebida
        fields = (
            'nombre', 'marca', 'precio', 'descuento', 'stock', 'enPromocion', 'activo', 'seccion')


    def __init__(self, *args, **kwargs):
        super(altaBebidaForm, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo

        #selecciono las secciones de la carta que son solo de platos
        seccionesChoice = SeccionCarta.objects.filter(categoria= 'B')
        #las formateo para crear un choice
        secciones = [(secc.id, secc.nombre) for secc in seccionesChoice]
        #indico que el widget tiene que mostrar el choice recien creado
        self.fields['seccion'].widget = Select(choices=secciones)

        #formateando los inputs
        ACTIVO = ((True, 'Activo'), (False, 'Inactivo'))
        self.fields['activo'].widget = Select(choices=ACTIVO)
        EN_PROMOCION = ((True, 'Si'), (False, 'No'))
        self.fields['enPromocion'].widget = Select(choices=EN_PROMOCION)