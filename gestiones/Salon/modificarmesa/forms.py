from django.forms import ModelForm, Select
from gestiones.Salon.altamesa.models import Mesa


class modificarMesa(ModelForm):
    class Meta:
        model = Mesa
        fields = (
            'tipo', 'capacidad', 'ocupada', 'activo', 'sector')


        def __init__(self, *args, **kwargs):
            super(modificarMesa, self).__init__(*args, **kwargs)
            self.fields['ocupada'].widget = Select()
            self.fields['activo'].widget = Select()