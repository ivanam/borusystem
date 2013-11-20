from datetime import time
from django.db import models
from django.template import defaulttags
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Mozo.models import Personal
from gestiones.Producto.producto.models import Plato, Ejecutivo, Bebida, DelDia
from gestiones.Salon.altamesa.models import Mesa
import datetime
from datetime import date
from time import time


ESTRATEGIAS = []


class EstrategiaServicio(object):

    def __init__(self, nombre, inicio, fin):
        self.inicio = inicio
        self.fin = fin
        self.nombre = nombre

    @classmethod
    def obtenerEstrategia(cls, comanda):
        for estrategia in ESTRATEGIAS:
            if estrategia.inicio < comanda.hora < estrategia.fin:
                return estrategia

    def cargarProductos(self, comanda, producto, cantidad):
        pass

    def facturar (self, comanda):
        pass

    def filtrar_secciones(self):
        pass

    #return self.estrategia.filtrar_secciones(secciones)

class EstrategiaComanda(EstrategiaServicio):

    def cargarProductos(self, comanda, producto, cantidad):
        detalle = DetalleComanda.objects.create(cantidadP=cantidad)
        if type(producto) is Plato:
            detalle.platos = producto
        else:
            if type(producto) is Bebida:
                detalle.bebidas = producto
            else:
                if type(producto) is DelDia:
                    detalle.menuD = producto
                else:
                    detalle.menuE = producto

        comanda.detalles.add(detalle)
        comanda.save()

    def facturar(self, comanda):
        pass

    def filtrar_secciones(self):
        seccion = SeccionCarta.objects.filter(activo__exact=1)
        return seccion

class EstrategiaPedido(EstrategiaServicio):
    def cargarProductos(self, comanda, producto, cantidad):
        detalle = DetalleComanda.objects.create(cantidadP=cantidad)
        if type(producto) is Bebida:
            detalle.bebidas = producto
        else:
            print("El producto no se puede cargar")

        comanda.detalles.add(detalle)
        comanda.save()

    def facturar(self, comanda):
        pass

    def filtrar_secciones(self):
        seccion = SeccionCarta.objects.filter(categoria__exact='B', activo__exact=1)
        return seccion



ESTRATEGIAS.append(EstrategiaPedido("Pub", datetime.time(0, 0, 0), datetime.time(6, 59, 59)))
ESTRATEGIAS.append(EstrategiaComanda("Resto", datetime.time(7, 0, 0), datetime.time(23, 59, 59)))

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
    mesas = models.ManyToManyField(Mesa, related_name="ocupa", null=True, blank=True)
    mozo = models.ForeignKey(Personal,null=True, blank=True)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.estrategia = EstrategiaServicio.obtenerEstrategia(self)
        print ("seteadas estrategias")

    def filtrar_secciones(self):
        return self.estrategia.filtrar_secciones()

    def cargar_mesas (self, mesa):
        self.mesas.add(mesa)
        mesa.ocupada = True
        mesa.save()
        self.save()

    def sacar_mesas (self, mesa):
        self.mesas.remove(mesa)
        mesa.ocupada = False
        mesa.save()
        self.save()
