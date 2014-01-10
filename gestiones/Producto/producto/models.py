# -*- encoding: utf-8 -*-
from django.db import models


class Producto(models.Model):
    ACTIVO_CHOICES = ((True, 'Activo'), (False, 'Inactivo'))

    nombre = models.CharField("Nombre", max_length=50)
    precio = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    stock = models.PositiveIntegerField("Stock", max_length=3)
    activo = models.BooleanField("Activo", default=True, choices=ACTIVO_CHOICES)
    seccion = models.ForeignKey("altacarta.SeccionCarta", null=False, blank=False)

    class Meta:
        abstract = True

    def cambiarEstado(self):
        if self.activo:
            self.activo = False
        else:
            self.activo = True


class Plato(Producto):
    PROMOCION_CHOICES = ((True, 'Si'), (False, 'No'))
    DESCUENTO_CHOICES = (
        (0, "00%"), (05, "05%"), (10, "10%"), (15, "15%"), (20, "20%"), (25, "25%"), (30, "30%"), (35, "35%"),
        (40, "40%"), (45, "45%"), (50, "50%"), (55, "55%"), (60, "60%"), (65, "65%"), (70, "70%"), (75, "75%"),
        (80, "80%"), (85, "85%"), (90, "90%"), (95, "95%"), (100, "100%"))

    descripcion = models.CharField("Descripcion", max_length=100, null=True, blank=True)
    enPromocion = models.BooleanField("En_Promocion", default=False, null=False, blank=True, choices=PROMOCION_CHOICES)
    descuento = models.DecimalField("Descuento", null=True, blank=True, choices=DESCUENTO_CHOICES, default=0,
                                    max_digits=11, decimal_places=0)

    def importe(self):

        if self.enPromocion:
            importe_descontado = ((self.precio * self.descuento) / 100)
        else:
            importe_descontado = 0

        return self.precio - importe_descontado


class Bebida(Producto):
    PROMOCION_CHOICES = ((True, 'Si'), (False, 'No'))
    DESCUENTO_CHOICES = (
        (0, "00%"), (05, "05%"), (10, "10%"), (15, "15%"), (20, "20%"), (25, "25%"), (30, "30%"), (35, "35%"),
        (40, "40%"), (45, "45%"), (50, "50%"), (55, "55%"), (60, "60%"), (65, "65%"), (70, "70%"), (75, "75%"),
        (80, "80%"), (85, "85%"), (90, "90%"), (95, "95%"), (100, "100%"))

    marca = models.CharField("Marca", max_length=20, null=True, blank=True)
    enPromocion = models.BooleanField("En_Promocion", default=False, null=False, blank=True, choices=PROMOCION_CHOICES)
    descuento = models.DecimalField("Descuento", null=True, blank=True, choices=DESCUENTO_CHOICES, default=0,
                                    max_digits=11, decimal_places=0)

    def importe(self):

        if self.enPromocion:
            importe_descontado = ((self.precio * self.descuento) / 100)
        else:
            importe_descontado = 0

        return self.precio - importe_descontado


class Menu(Producto):
    descripcion = models.CharField("Descripcion", max_length=100, null=True, blank=True)
    fecha_Inicio = models.DateField("Fecha_Inicio")
    platos = models.ManyToManyField(Plato, null=False, blank=False)

    class Meta:
        abstract = True

    def importe(self):
        return self.precio

class DelDia(Menu):
    pass


class Ejecutivo(Menu):
    fecha_fin = models.DateField("Fecha_Fin")


class MenuS(object):
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.total = (precio * int(cantidad))
