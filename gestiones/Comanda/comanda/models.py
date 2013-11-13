from datetime import time
from django.db import models
from gestiones.Mozo.models import Personal
from gestiones.Producto.producto.models import Plato, Ejecutivo, Bebida, DelDia
from gestiones.Salon.altamesa.models import Mesa

ESTRATEGIAS = []


class EstrategiaServicio(models.Model):
    nombre = models.CharField("Nombre", max_length=50)
    hora_inicio = models.TimeField("Inicio", null=True, blank=True)
    hora_fin = models.TimeField("Fin", null=True, blank=True)

    class Meta:
        abstract = True

    @classmethod
    def obtenerEstrategia(cls, comanda):
        for estrategia in ESTRATEGIAS:
            if estrategia.inicio < comanda.hora < estrategia.fin:
                return estrategia



class EstrategiaComanda(EstrategiaServicio):
    pass

class EstrategiaPedido(EstrategiaServicio):
    pass

ESTRATEGIAS.append(EstrategiaPedido("Pub", time(0), time(6, 59)))
ESTRATEGIAS.append(EstrategiaComanda("Resto", time(7), time(23, 59)))

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
    estrategiaC = models.ForeignKey(EstrategiaComanda, null=True, blank=True)
    estrategiaP = models.ForeignKey(EstrategiaPedido, null=True, blank=True)
    mesas = models.ManyToManyField(Mesa, related_name="ocupa", null=True, blank=True)
    mozo = models.ForeignKey(Personal,null=True, blank=True)


