from django.forms import ModelForm, Select, Textarea
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Plato


class stockPlato(ModelForm):
    class Meta:
        model = Plato
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'enPromocion', 'descuento', 'seccion', 'activo')




