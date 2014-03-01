from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission
from django.forms.widgets import PasswordInput, Select
from gestiones.Administrador.models import permisosVistas


class modificarusuarioForm(ModelForm):
    content_type = ContentType.objects.get_for_model(permisosVistas)
    permisoUsuarios = Permission.objects.filter(content_type=content_type, codename__icontains='is_')
    permisos = forms.ModelMultipleChoiceField(permisoUsuarios,required=True,help_text="Seleccione varios permisos con la tecla Ctrl")

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'tipoDoc', 'numeroDoc', 'telefono',
                  'direccion', 'turno', 'is_active')



    def __init__(self, *args, **kwargs):
        super(modificarusuarioForm, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages = {'required': 'El nombre de Usuario no es valido!'}
        self.fields['password'].error_messages = {'required': 'El password ingresado no es valido!'}
        self.fields['email'].error_messages = {'required': 'La direccion de E-mail ingresada no es correcta!'}

        self.fields['password'].widget = PasswordInput()
        ACTIVO = ((True, 'Activo'), (False, 'Inactivo'))
        self.fields['is_active'].widget = Select(choices=ACTIVO)
        self.fields['numeroDoc'].widget.attrs['maxlength'] = 8
        self.fields['permisos'].widget.attrs['class'] = 'permisosSelect centrar'
