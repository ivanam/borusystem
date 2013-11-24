from django.contrib.auth.models import User
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

    def facturar(self, comanda):
        pass

    def filtrar_secciones(self):
        pass

    def finalizar_comanda(self, comanda):
        pass

        #return self.estrategia.filtrar_secciones(secciones)

    def cerrar_comanda(self,comanda):
        pass

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

    def finalizar_comanda(self, comanda):
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
        print("Aca creo la factura")
        factura = Factura.objects.create(fecha=fecha, hora=hora, tipo='C', total=total, comanda=comanda)
        for detalles in comanda.detalles.all():
            print("Cargo detalle")
            total = total + detalles.importe()
            detalleF = detalles.covertir_factura()
            print("cargo detalle en fact")
            factura.detalle.add(detalleF)

        print("cargo total")
        factura.total = total
        factura.save()
        comanda.save()
        #TODO el facturar es comun a los dos tipos de comanda hay que subirlo
        #y de finalizar comanda llamarlo haciendo uso del facturar

ESTRATEGIAS.append(EstrategiaPedido("Pub", datetime.time(0, 0, 0), datetime.time(6, 59, 59)))
ESTRATEGIAS.append(EstrategiaComanda("Resto", datetime.time(7, 0, 0), datetime.time(23, 59, 59)))


class DetalleComanda(models.Model):
    cantidadP = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    entregado = models.BooleanField("Entregado", default=False)
    platos = models.ForeignKey(Plato, null=True, blank=True)
    bebidas = models.ForeignKey(Bebida, null=True, blank=True)
    menuD = models.ForeignKey(DelDia, null=True, blank=True)
    menuE = models.ForeignKey(Ejecutivo, null=True, blank=True)

    def importe(self):
        detalleImporte = 0

        if (self.platos) != None:
            detalleImporte = self.platos.importe() * self.cantidadP
        else:
            if (self.bebidas) != None:
                detalleImporte = self.bebidas.importe() * self.cantidadP
            else:
                if (self.menuD) != None:
                    detalleImporte = self.menuD.precio * self.cantidadP
                else:
                    detalleImporte = self.menuE.precio * self.cantidadP

        return detalleImporte

    def covertir_factura(self):
        if (self.platos) != None:
            precio = self.platos.importe()
        else:
            if (self.bebidas) != None:
                precio = self.bebidas.importe()
            else:
                if (self.menuD) != None:
                    precio = self.menuD.precio()
                else:
                    if (self.menuE) != None:
                        precio = self.menuE.precio()

        detalle = DetalleFactura.objects.create(cantidad=self.cantidadP, precioXunidad=precio, detalleComanda=self)
        return detalle


class Comanda(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    cantidadC = models.DecimalField("CantidadC", max_digits=11, decimal_places=0)
    cerrada = models.BooleanField("Cerrada", default=False)
    detalles = models.ManyToManyField(DetalleComanda, related_name="tiene", null=True, blank=True)
    mesas = models.ManyToManyField(Mesa, related_name="ocupa", null=True, blank=True)
    mozo = models.ForeignKey(User, null=True, blank=True)
    vista = models.BooleanField("Vista", default=False)
    finalizada=models.BooleanField("Finalizada", default=False)
    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.estrategia = EstrategiaServicio.obtenerEstrategia(self)
        print ("seteadas estrategias")

    def total(self):
        aux=0
        for  c in self.detalles.all():
            aux = aux + c.importe()

        return aux

    def filtrar_secciones(self):
        return self.estrategia.filtrar_secciones()

    def cargar_mesas(self, mesa):
        self.mesas.add(mesa)
        mesa.ocupada = True
        mesa.save()
        self.save()

    def sacar_mesas(self, mesa):
        self.mesas.remove(mesa)
        mesa.ocupada = False
        mesa.save()
        self.save()

    def finalizar(self):
        self.estrategia.finalizar_comanda(self)


class DetallePreticket(models.Model):
    cantidad = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    precioXunidad = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    detalleComanda = models.ForeignKey(DetalleComanda)


class Preticket(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    total = models.DecimalField("Total", max_digits=11, decimal_places=2)
    comanda = models.ForeignKey(Comanda)
    detalles = models.ManyToManyField(DetallePreticket, related_name="compuesto", null=True, blank=True)


class DetalleFactura(models.Model):
    cantidad = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    precioXunidad = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    detalleComanda = models.ForeignKey(DetalleComanda, null=True, blank=True)
    detallePreticket = models.ForeignKey(DetallePreticket, null=True, blank=True)


class Factura(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    tipo = models.CharField("Tipo", choices=TIPO, max_length=1)
    total = models.DecimalField("Total", max_digits=11, decimal_places=2)
    detalle = models.ManyToManyField(DetalleFactura, related_name="contiene", null=True, blank=True)
    comanda = models.ForeignKey(Comanda, null=True, blank=True)
    preticket = models.ForeignKey(Preticket, null=True, blank=True)


class DetallePago(models.Model):
    importe = models.DecimalField("importe", max_digits=11, decimal_places=2)
    tipoPago = models.CharField("Tipo", choices=TIPO_PAGO, max_length=2)


class Pago(models.Model):
    fecha = models.DateField("Fecha")
    factura = models.ForeignKey(Factura)