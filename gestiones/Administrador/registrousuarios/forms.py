from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm, Select, PasswordInput
from django.contrib.auth.models import User, Permission
from gestiones.Administrador.models import permisosVistas


class registrousuariosForm(ModelForm):

    content_type = ContentType.objects.get_for_model(permisosVistas)
    permisoUsuarios = Permission.objects.filter(content_type=content_type,codename__icontains = 'is_')
    permisos = forms.ModelChoiceField(permisoUsuarios,empty_label="--------",required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'first_name', 'last_name', 'email', 'tipoDoc', 'numeroDoc', 'telefono', 'direccion',
            'turno', 'is_active')

    def __init__(self, *args, **kwargs):
        super(registrousuariosForm, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo

        #manejo de mensajes de error
        self.fields['username'].error_messages = {'required': 'El nombre de Usuario no es valido!'}
        self.fields['password'].error_messages = {'required': 'El password ingresado no es valido!'}
        self.fields['email'].error_messages = {'required': 'La direccion de E-mail ingresada no es correcta!'}


        #formateando los inputs
        ACTIVO = ((True, 'Activo'), (False, 'Inactivo'))
        self.fields['is_active'].widget = Select(choices=ACTIVO)

        self.fields['password'].widget = PasswordInput()

        #agregando max-length
        self.fields['numeroDoc'].widget.attrs['maxlength'] = 8


        #self.fields['tipoDoc'].widget = Select()
        #self.fields['turno'].widget = Select()
        #self.fields['activo'].widget = Select()
        #self.fields['password'].error_messages= 'Passoword Incorrecto!'
        #self.fields['password'].help_text= 'Password con el cual se va a loguear en el sistema!'
        #Aniadimos class="claseCSS" a la etiqueta HTML que corresponda al tipo de dato
        #self.fields['campo1'].widget.attrs['class'] = 'claseCSS'
        #Vamos a cambiar el 'This field is required' que trae Django por defecto para un campo que es obligatorio rellenarlo por 'Este campo es obligatorio y lo vamos a hacer para todos los campos de este formulario.
        #for field in self.fields:
        #   self.fields[field].error_messages = {'required': 'Este campo es obligatorio!'}


