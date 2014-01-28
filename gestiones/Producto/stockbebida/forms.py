# -*- encoding: utf-8 -*-
from django.forms import ModelForm, TextInput
from gestiones.Producto.producto.models import Bebida

class stockBebida(ModelForm):

    class Meta:
        model = Bebida
        fields = (
            'nombre', 'precio', 'stock')


    def __init__(self, *args, **kwargs):
        super(stockBebida, self).__init__(*args, **kwargs)

        for field in self.fields:
           self.fields[field].widget = TextInput(attrs={'readonly': True})