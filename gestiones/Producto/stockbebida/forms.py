# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Select
from gestiones.Producto.producto.models import Bebida


class stockBebida(ModelForm):
    class Meta:
        model = Bebida
        fields = (
          'nombre', 'precio', 'stock', 'enPromocion', 'descuento', 'seccion', 'activo')

