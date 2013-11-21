from django.db import models
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Mozo.models import Personal
from gestiones.Producto.producto.models import Plato, Ejecutivo, Bebida, DelDia
from gestiones.Salon.altamesa.models import Mesa
import datetime


ESTRATEGIAS = []

TIPO = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

TIPO_PAGO = (
    ('E', 'Efectivo'),
    ('TD', 'Tarjeta_debito'),
    ('TC', 'Tarjeta_credito'),
)


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

    def finalizar_comanda(self):
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

    def finalizar_comanda(self):
        pass

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

    def finalizar_comanda(self, comanda):
        comanda.cerrada = True
        fecha = datetime.date.today()
        now = datetime.datetime.now()
        hora = datetime.time(now.hour, now.minute, now.second)
        total = 0
        for platos in comanda.detalles.platos:
            total = total + platos.importe
        for bebidas in comanda.detalles.bebidas:
            total = total + bebidas.importe
        for menuD in comanda.detalles.menuD:
            total = total + menuD.precio
        for mennuE in comanda.detalles.menuE:
            pass



ESTRATEGIAS.append(EstrategiaPedido("Pub", datetime.time(0, 0, 0), datetime.time(6, 59, 59)))
ESTRATEGIAS.append(EstrategiaComanda("Resto", datetime.time(7, 0, 0), datetime.time(23, 59, 59)))

class DetalleComanda(models.Model):
    cantidadP = models.IntegerField("CantidadP")
    entregado = models.BooleanField("Entregado", default=False)
    platos = models.ForeignKey(Plato, null=True, blank=True)
    bebidas = models.ForeignKey(Bebida, null=True, blank=True)
    menuD = models.ForeignKey(DelDia, null=True, blank=True)
    menuE = models.ForeignKey(Ejecutivo, null=True, blank=True)

    def importe(self):
       detalleImporte=0.00

       if len(self.platos) != 0:
           detalleImporte = self.platos.importe()*self.cantidadP
       else:
           if len(self.bebidas) != 0:
               detalleImporte = self.bebidas.importe() * self.cantidadP
           else:
               if len(self.menuD) != 0:
                   detalleImporte = self.menuD.importe() * self.cantidadP
               else:
                   if len(self.menuE) != 0:
                       detalleImporte = self.menuE.importe() * self.cantidadP

       return detalleImporte

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


class DetallePreticket(models.Model):
    cantidad = models.IntegerField("CantidadP")
    precioXunidad = models.FloatField("Precio")
    detalleComanda = models.ForeignKey(DetalleComanda)

class Preticket(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    total = models.FloatField("Total")
    comanda = models.ForeignKey(Comanda)
    detalles = models.ManyToManyField(DetallePreticket, related_name="compuesto", null=True, blank=True)

class DetalleFactura(models.Model):
    cantidad = models.IntegerField("CantidadP")
    precioXunidad = models.FloatField("Precio")
    detalleComanda = models.ForeignKey(DetalleComanda, null=True, blank=True)
    detallePreticket = models.ForeignKey(DetallePreticket, null=True, blank=True)


class Factura(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    tipo = models.CharField("Tipo", choices=TIPO, max_length=1)
    total = models.FloatField("Total")
    detalle = models.ManyToManyField(DetalleFactura, related_name="contiene", null=True, blank=True)
    comanda = models.ForeignKey(Comanda, null=True, blank=True)
    preticket = models.ForeignKey(Preticket, null=True, blank=True)

class DetallePago(models.Model):
    importe = models.FloatField("importe")
    tipoPago = models.CharField("Tipo", choices=TIPO_PAGO, max_length=2)

class Pago(models.Model):
    fecha = models.DateField("Fecha")
    factura = models.ForeignKey(Factura)