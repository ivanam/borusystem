from django.db import models
from gestiones.Producto.producto.models import Plato, Bebida, DelDia, Ejecutivo

CATEGORIA = (
    ('P', 'Plato'),
    ('B', 'Bebida'),
    ('M', 'Menu'),
)

class SeccionCarta(models.Model):
    nombre = models.CharField('Nombre', max_length=30, blank=True)
    categoria = models.CharField('Categoria', max_length=1, choices=CATEGORIA)
    activo = models.BooleanField('Activo', default=True)
    cartavigente = models.ForeignKey('Carta')
    platoss = models.ManyToManyField(Plato, null=True, related_name='contiene1')
    bebidas = models.ManyToManyField(Bebida, null=True, related_name='contiene2')
    menuesD = models.ManyToManyField(DelDia, null=True, related_name='contiene3')
    menuesE = models.ManyToManyField(Ejecutivo, null=True, related_name='contiene3')

    def __str__(self):
        return self.nombre

class Carta(models.Model):
    nombre = models.CharField('Nombre', max_length=30)
    vigente = models.BooleanField('Vigente')
    fecha = models.DateField('Fecha',blank=True)
    secciones = models.ManyToManyField('SeccionCarta', null=True,related_name='compuesta')






