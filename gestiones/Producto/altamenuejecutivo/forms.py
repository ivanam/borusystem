from django.forms import ModelForm, Textarea, CheckboxInput, CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, Select
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Ejecutivo


class altaMenuEjecutivoForm(ModelForm):
    class Meta:
        model = Ejecutivo
        fields = (
            'nombre', 'precio', 'stock', 'descripcion', 'fecha_Inicio','fecha_fin', 'seccion', 'platos')

    def __init__(self, *args, **kwargs):

            super(altaMenuEjecutivoForm, self).__init__(*args, **kwargs)

            #selecciono las secciones de la carta que son solo de platos
            seccionesChoice = SeccionCarta.objects.filter(categoria='E')
            #las formateo para crear un choice
            secciones = [(secc.id, secc.nombre) for secc in seccionesChoice]
            #indico que el widget tiene que mostrar el choice recien creado
            self.fields['seccion'].widget = Select(choices=secciones)

            self.fields['descripcion'].widget = Textarea(attrs={'rows': 3})

            self.fields['platos'].widget = CheckboxSelectMultiple()
