from django.db import models
from gestiones.Mozo.models import Personal
from gestiones.Producto.producto.models import Plato, Ejecutivo, Bebida, DelDia
from gestiones.Salon.altamesa.models import Mesa

class EstrategiaServicio(models.Model):
    nombre = models.CharField("Nombre", max_length=50)
    hora_inicio = models.TimeField("Inicio")
    hora_fin = models.TimeField("Fin")
    class Meta:
        abstract = True


class EstrategiaComanda(EstrategiaServicio):
    pass

class EstrategiaPedido(EstrategiaServicio):
    pass

class DetalleComanda(models.Model):
    cantidadP = models.IntegerField("CantidadP")
    entregado = models.BooleanField("Entregado", default=False)
    platos = models.ForeignKey(Plato, null=True, blank=True)
    bebidas = models.ForeignKey(Bebida, null=True, blank=True)
    menuD = models.ForeignKey(DelDia, null=True, blank=True)
    menuE = models.ForeignKey(Ejecutivo, null=True, blank=True)


class Comanda(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    cantidadC = models.IntegerField("CantidadC")
    cerrada = models.BooleanField ("Cerrada", default=False)
    detalles = models.ManyToManyField(DetalleComanda, related_name="tiene", null=True, blank=True)
    estrategiaC = models.ForeignKey(EstrategiaComanda)
    estrategiaP = models.ForeignKey(EstrategiaPedido)
    mesas = models.ManyToManyField(Mesa, related_name="ocupa", null=True, blank=True)
    mozo = models.ForeignKey(Personal)


