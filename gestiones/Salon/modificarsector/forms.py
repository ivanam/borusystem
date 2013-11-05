from django.forms import ModelForm, Select
from gestiones.Salon.altamesa.models import Sector


class modificarSectorForm(ModelForm):
    class Meta:
        model = Sector
        fields = (
            'id','descripcion', 'tipo', 'activo', 'mesas')

        def __init__(self, *args, **kwargs):
            super(modificarSectorForm, self).__init__(*args, **kwargs) #Esto siempre hay que ponerlo
            #self.fields['activo'].widget = Select()
            #self.fields['activo'].widget = Select()