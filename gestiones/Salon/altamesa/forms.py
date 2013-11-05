from django.forms import ModelForm, Select
from gestiones.Salon.altamesa.models import Mesa


class altaMesaForm(ModelForm):
    class Meta:
        model = Mesa
        fields = (
            'tipo', 'capacidad', 'ocupada', 'activo', 'sector')

#        def __init__(self, *args, **kwargs):
 #           super(altaMesaForm, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo

        #self.fields['ocupada'].error_messages = {'required': 'El nombre de Usuario no es valido!'}
        #self.fields['password'].error_messages = {'required': 'El password ingresado no es valido!'}
        #self.fields['email'].error_messages = {'required': 'La direccion de E-mail ingresada no es correcta!'}
  #          self.fields['ocupada'].widget = Select()
   #         self.fields['activo'].widget = Select()

        #self.fields['numero'].error_messages = {'required': 'El numero de la mesa no es valido!'}

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
