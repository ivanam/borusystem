from django import forms
from django.forms import ModelForm, Select, Textarea, CheckboxSelectMultiple
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Ejecutivo



class modificarMenuEjecutivoForm(ModelForm):
    class Meta:
        model = Ejecutivo
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'fecha_Inicio', 'fecha_fin', 'seccion','activo','platos')


    def clean_precio(self):
        diccionario_limpio = self.cleaned_data

        precio = diccionario_limpio.get('precio')

        if precio < 0:
            raise forms.ValidationError("El precio no puede ser menor a cero.")

        return precio

    def clean_fecha(self):

        diccionario_limpio = self.cleaned_data

        fecha_fin = diccionario_limpio.get('fecha_fin')
        fecha_Inicio = diccionario_limpio.get('fecha_Inicio')

        if (fecha_Inicio > fecha_fin) :

            raise forms.ValidationError("La Fecha Fin no puede ser menor a la fecha de inicio")

        return fecha_fin


    def __init__(self, *args, **kwargs):

                super(modificarMenuEjecutivoForm, self).__init__(*args, **kwargs)

                #selecciono las secciones de la carta que son solo de platos
                seccionesChoice = SeccionCarta.objects.filter(categoria='D')
                #las formateo para crear un choice
                secciones = [(secc.id, secc.nombre) for secc in seccionesChoice]
                #indico que el widget tiene que mostrar el choice recien creado
                self.fields['seccion'].widget = Select(choices=secciones)

                self.fields['descripcion'].widget = Textarea(attrs={'rows': 3})

                self.fields['platos'].widget = CheckboxSelectMultiple()