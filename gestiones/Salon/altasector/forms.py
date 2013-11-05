from django.forms import ModelForm, Select
from gestiones.Salon.altamesa.models import Sector


class altaSectorForm(ModelForm):
    class Meta:
        model = Sector
        fields = (
            'descripcion', 'tipo', 'activo', 'mesas')