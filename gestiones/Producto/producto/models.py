from django.db import models

class Producto(models.Model):
    nombre = models.CharField("Nombre", max_length=50)
    precio = models.FloatField("Precio")
    stock = models.IntegerField("Stock")
    activo = models.BooleanField("Activo", default=True)
    seccion = models.ForeignKey("altacarta.SeccionCarta", null=False, blank=False)
    class Meta:
        abstract = True

class Plato(Producto):
    descripcion = models.CharField("Descripcion", max_length=100, null=True, blank=True)
    enPromocion = models.BooleanField("En_Promocion", default=False)
    descuento = models.FloatField("Descuento", null=True, blank=True)

class Bebida(Producto):
    marca = models.CharField("Marca", max_length=20, null=True, blank=True)
    enPromocion = models.BooleanField("En_Promocion", default=False)
    descuento = models.FloatField("Descuento", null=True)

class Menu(Producto):
    descripcion = models.CharField("Descripcion", max_length=100, null=True, blank=True)
    fecha_Inicio = models.DateField("Fecha_Inicio")
    platos = models.ManyToManyField(Plato, null=False, blank=False)

    class Meta:
        abstract = True

class DelDia(Menu):
    pass

class Ejecutivo(Menu):
    fecha_fin = models.DateField("Fecha_Fin")

class MenuS(object):

    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.total = (precio*float(cantidad))
