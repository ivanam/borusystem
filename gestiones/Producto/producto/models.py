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

    def __str__(self):
        return self.nombre

    def cambiarEstado(self):
        if self.activo:
            self.activo = False

            #rescato los menues del dia en los que esta el plato
            menuDia = self.estoyEnMenuDia()
            #los recorro para desactivarlos
            for md in menuDia:
                md.activo = False
                md.save()

            #lo mismo para los menues ejecutivos
            menuEje = self.estoyEnMenuEjecutivo()
            #los recorro para desactivarlos
            for me in menuEje:
                me.activo = False
                me.save()


        else:
            self.activo = True

    def estoyEnMenuDia(self):
        #lista de menues donde estoy
        listaMenus = []
        #busco los menues del dia
        menuDia = DelDia.objects.all()
        #los recorro
        for m in menuDia:
            #rescato los platos del menu
            menuPlatos = m.platos.all()
            #me fijo si estoy en la lista de platos del menu
            if self in menuPlatos.all():
                #si estoy agrego el menu en la lista
                listaMenus.append(m)

        #si estoy en algun menu devuelvo una lista de menues donde estoy
        return listaMenus

    def estoyEnMenuEjecutivo(self):
        #lista de menues donde estoy
        listaMenus = []
        #busco los menues ejecutivos
        menuEjecutivo = Ejecutivo.objects.all()
        #los recorro
        for m in menuEjecutivo:
            #rescato los platos del menu
            menuPlatos = m.platos.all()
            #me fijo si estoy en la lista de platos del menu
            if self in menuPlatos.all():
                #si estoy agrego el menu en la lista
                listaMenus.append(m)

        #si estoy en algun menu devuelvo una lista de menues donde estoy
        return listaMenus


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
    stockAgregado = models.PositiveIntegerField("Stock", max_length=3, null = True)

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

    stockAgregado = models.PositiveIntegerField("Stock", max_length=3, null = True)

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

    def limpiar_platos(self):
        self.platos = []
        self.save()

    def agregar_plato(self, plato):
        #no puede haber platos repetidos
        try:
            self.platos.remove(plato)
        except:
            pass

        self.platos.add(plato)
        self.save()

    def eliminar_plato(self, plato):
        try:
            self.platos.remove(plato)
        except:
            pass

        self.save()


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
