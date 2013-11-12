from django.forms import ModelForm
from django.forms.widgets import Select
from gestiones.Carta.altacarta.models import Carta


class altaCartaForm(ModelForm):
    class Meta:
        model = Carta
        fields = (
            'nombre', 'vigente')


    def __init__(self, *args, **kwargs):
        super(altaCartaForm, self).__init__(*args, **kwargs)
        vigente = ((True, 'vigente'), (False, 'No vigente'))
        self.fields['vigente'].widget = Select(choices=vigente)


