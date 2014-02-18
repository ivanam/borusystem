import datetime
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q


class historicoVentasForm(forms.Form):
    CRITERIO_LISTADO = (
        ('t', 'Todos'),
        ('ca', 'Solo Comandas Abiertas'),
        ('cc', 'Solo Comandas Cerradas'),
        ('p', 'Solo Pedidos'),
        ('ptk', 'Solo Pretickets'),
        ('f', 'Todas las Facturas'),
        ('fp', 'Solo Facturas Pagas'),
        ('fnp', 'Solo Facturas no Pagas')
    )

    hoy = datetime.date.today()
    ayer = datetime.date.today() - datetime.timedelta(days=1)

    fecha_Inicio = forms.DateField(required=True, widget=forms.TextInput(attrs={'class': 'input-small'}), initial=ayer)
    fecha_fin = forms.DateField(required=True, widget=forms.TextInput(attrs={'class': 'input-small'}), initial=hoy)
    criterio_listado = forms.ChoiceField(required=True, choices=CRITERIO_LISTADO, initial='Todos')
    historico_page = forms.CharField(required=True, widget=forms.HiddenInput, initial=1)

    query_set_mozos = User.objects.filter(Q(user_permissions__codename="is_mozo") | Q(is_superuser=True) ).order_by('username', '-is_active')
    mozo = forms.ModelChoiceField(queryset=query_set_mozos,required=False,empty_label="Todos")

    def clean_fecha_fin(self):
        diccionario_limpio = self.cleaned_data

        fecha_fin = diccionario_limpio.get('fecha_fin')
        fecha_Inicio = diccionario_limpio.get('fecha_Inicio')

        if (fecha_Inicio > fecha_fin):
            raise forms.ValidationError("La Fecha Fin no puede ser menor a la fecha de inicio")

        return fecha_fin




