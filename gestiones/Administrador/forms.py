import datetime
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, Select

class altaUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'is_active')


    def __init__(self, *args, **kwargs):
        super(altaUsuarioForm, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo

        #manejo de mensajes de error
        self.fields['username'].error_messages = {'required': 'El nombre de Usuario no es valido!'}
        self.fields['password'].error_messages = {'required': 'El password ingresado no es valido!'}
        self.fields['email'].error_messages = {'required': 'La direccion de E-mail ingresada no es correcta!'}

        #formateando los inputs
        ACTIVO = ((True, 'Activo'), (False, 'Inactivo'))
        self.fields['is_active'].widget = Select(choices=ACTIVO)
        self.fields['password'].widget = PasswordInput()


class fechasXconsultaForm(forms.Form):

    GRAFICOS_TIPO = (
        ('area', 'Areas'),
        ('bar', 'Barras'),
        ('column', 'Columnas'),
        ('line', 'Lineas'),
        ('pie', 'Torta'),
        ('radar', 'Radial'),
        ('scatter', 'Dispersion')
    )

    PRODUCTO_INFORME = (
        ('TODOS','Todos los productos'),
        ('plato', 'Solo Platos'),
        ('bebida', 'Solo Bebidas'),
        ('deldia', 'Solo Menues del Dia'),
        ('ejecutivo', 'Solo Menues Ejecutivos')
    )

    TOP_PRODUCTOS = (
        ('ALL','Todos'),
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
        ('25', '25'),
        ('30', '30'),
        ('35', '35'),
        ('40', '40'),
        ('45', '45'),
        ('50', '50')
    )

    CRITERIO_CONSULTA = (
        ('MAS', 'Productos mas vendidos'),
        ('MENOS', 'Productos menos vendidos')
    )

    hoy = datetime.date.today()

    fecha_Inicio = forms.DateField(required=True,widget = forms.TextInput, initial=hoy)
    fecha_fin = forms.DateField(required=True,widget = forms.TextInput)
    tipo_grafico = forms.ChoiceField(required=True, choices=GRAFICOS_TIPO, initial='pie')
    producto_informe = forms.ChoiceField(required=True, choices=PRODUCTO_INFORME, initial='TODOS')
    top_productos = forms.ChoiceField(required=True, choices=TOP_PRODUCTOS, initial='15')
    criterio_consulta = forms.ChoiceField(required=True, choices=CRITERIO_CONSULTA, initial='MAS')

    def clean_fecha_fin(self):
        diccionario_limpio = self.cleaned_data

        fecha_fin = diccionario_limpio.get('fecha_fin')
        fecha_Inicio = diccionario_limpio.get('fecha_Inicio')

        if (fecha_Inicio > fecha_fin):
            raise forms.ValidationError("La Fecha Fin no puede ser menor a la fecha de inicio")

        return fecha_fin



class fechasXconsultaFacturasForm(forms.Form):

    hoy = datetime.date.today()

    fecha_Inicio = forms.DateField(required=True,widget = forms.TextInput, initial=hoy)
    fecha_fin = forms.DateField(required=True,widget = forms.TextInput)

    def clean_fecha_fin(self):
        diccionario_limpio = self.cleaned_data

        fecha_fin = diccionario_limpio.get('fecha_fin')
        fecha_Inicio = diccionario_limpio.get('fecha_Inicio')

        if (fecha_Inicio > fecha_fin):
            raise forms.ValidationError("La Fecha Fin no puede ser menor a la fecha de inicio")

        return fecha_fin
