# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Select
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Bebida


class altaBebidaForm(ModelForm):
    class Meta:
        model = Bebida
        fields = (
            'nombre', 'marca', 'precio', 'descuento', 'stock', 'enPromocion', 'activo', 'seccion')


        #Validamos que el autor no sea menor a 3 caracteres

    def clean_precio(self):
        diccionario_limpio = self.cleaned_data

        precio = diccionario_limpio.get('precio')

        if precio < 0:
            raise forms.ValidationError("El precio no puede ser menor a cero.")

        return precio

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