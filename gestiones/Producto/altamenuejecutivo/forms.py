from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, Select
from gestiones.Producto.producto.models import Ejecutivo


class altaMenuEjecutivoForm(ModelForm):
    class Meta:
        model = Ejecutivo
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'fecha_Inicio')

