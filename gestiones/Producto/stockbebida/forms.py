# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Select
from gestiones.Producto.producto.models import Bebida


class stockBebida(ModelForm):
    class Meta:
        model = Bebida
        fields = (
          'nombre', 'precio', 'stock', 'enPromocion', 'descuento', 'seccion', 'activo','stockAgregado')

    def clean_stock(self):
        diccionario_limpio = self.cleaned_data

        stock = diccionario_limpio.get('stock')

        if stock< 0:
            raise forms.ValidationError("El stock no puede ser menor a cero.")

        return stock



        #formateando los inputs
