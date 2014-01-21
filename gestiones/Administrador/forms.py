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
