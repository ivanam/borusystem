from django.forms import ModelForm, Select, Textarea
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Plato


class modificarPlato(ModelForm):
    class Meta:
        model = Plato
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'enPromocion', 'descuento', 'seccion', 'activo')


    def __init__(self, *args, **kwargs):
        super(modificarPlato, self).__init__(*args, **kwargs)

        #selecciono las secciones de la carta que son solo de platos
        seccionesChoice = SeccionCarta.objects.filter(categoria='P')
        #las formateo para crear un choice
        secciones = [(secc.id, secc.nombre) for secc in seccionesChoice]
        #indico que el widget tiene que mostrar el choice recien creado
        self.fields['seccion'].widget = Select(choices=secciones)

        self.fields['descripcion'].widget = Textarea(attrs={'rows': 3})
