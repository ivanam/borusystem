from django.forms import ModelForm
from django.forms.widgets import Select
from gestiones.Comanda.comanda.models import EstrategiaComanda


class altaEstrategiaComandaForm(ModelForm):
    class Meta:
        model = EstrategiaComanda
        fields = (
            'hora_inicio', 'hora_fin')
