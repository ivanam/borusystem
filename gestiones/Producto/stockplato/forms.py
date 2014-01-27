from django.forms import ModelForm, Select
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Plato
from django import forms


class stockPlato(ModelForm):
    class Meta:
        model = Plato
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'enPromocion', 'descuento', 'seccion', 'activo' ,'stockAgregado')

    def clean_stock(self):
        diccionario_limpio = self.cleaned_data

        stock = diccionario_limpio.get('stock')

        if stock< 0:
            raise forms.ValidationError("El stock no puede ser menor a cero.")

        return stock









