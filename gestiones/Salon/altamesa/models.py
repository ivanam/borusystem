from collections import defaultdict
from django.db import models

TIPO = (
    ('F', 'Fumador'),
    ('NF', 'No Fumador'),
)

TIPO_MESA = (
    (1, 'Barra'),
    (2, 'Box'),
    (3, 'Mesa'),
)

ACTIVO = ((True, "Activo"), (False, "Inactivo"),)
OCUPADA = ((True, "Ocupada"), (False, "Libre"),)


class Sector(models.Model):
    descripcion = models.CharField("Descripcion",max_length=100)
    tipo = models.CharField("Tipo",max_length=2, choices=TIPO, default='NF')
    activo = models.BooleanField("Activo",choices=ACTIVO,default=True)
    mesas = models.ManyToManyField('Mesa',verbose_name="Mesas", related_name='tiene',null=True,blank=True)

    def __str__(self):
        return self.descripcion

    def cambiarEstado(self):
        if self.activo:
            self.activo=False
        else:
            self.activo=True

class Mesa(models.Model):
    tipo = models.DecimalField(max_length=2, choices=TIPO_MESA, default=3, max_digits=11, decimal_places=0)
    capacidad = models.DecimalField("Capacidad", max_digits=11, decimal_places=0)
    ocupada = models.BooleanField("Ocupada", choices=OCUPADA, null=False, blank=False, default=False)
    activo = models.BooleanField("Activo", choices=ACTIVO, null=False, blank=False,default=True)
    sector = models.ForeignKey(Sector, null=False, blank=False, default=1)

    def cambiarEstado(self):
        if self.activo:
            self.activo = False
        else:
            self.activo = True