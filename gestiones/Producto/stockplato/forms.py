# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm, TextInput, Textarea
from gestiones.Producto.producto.models import Plato

class stockPlato(ModelForm):

    #addProducto = forms.IntegerField(label="Agregar Producto",error_messages="Introduzca solo numeros enteros.",widget=TextInput,required=True)

    class Meta:
        model = Plato
        fields = (
            'nombre', 'precio', 'stock', 'descripcion')


    def __init__(self, *args, **kwargs):
        super(stockPlato, self).__init__(*args, **kwargs)

        for field in self.fields:
           self.fields[field].widget = TextInput(attrs={'readonly': True})


        self.fields['descripcion'].widget = Textarea(attrs={'readonly': True,'rows': 3})













