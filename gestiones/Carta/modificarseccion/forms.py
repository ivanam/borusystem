from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, Select
from gestiones.Carta.altacarta.models import SeccionCarta


class modificarSeccionForm(ModelForm):
    class Meta:
        model = SeccionCarta
        fields = (
            'nombre','imagen')


