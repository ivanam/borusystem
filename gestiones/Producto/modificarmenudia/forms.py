from django.forms import ModelForm
from gestiones.Producto.producto.models import DelDia


class modificarMenuDiaForm(ModelForm):
    class Meta:
        model = DelDia
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'fecha_Inicio')

