from django.contrib.auth.models import User
from django.db import models
from gestiones.Carta.altacarta.models import SeccionCarta
from gestiones.Producto.producto.models import Plato, Ejecutivo, Bebida, DelDia
from gestiones.Salon.altamesa.models import Mesa
import datetime


ESTRATEGIAS = []

TIPO = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

TIPO_COMANDA = (
    ('C', 'Resto'),
    ('P', 'Pub')
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

    def __str__(self):
        return self.nombre

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

    def generar_preticket(self, comanda):
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
        comanda.finalizada = True
        comanda.save()


    def generar_preticket(self, comanda):

        print("comanda preticket")
        print(comanda.preticket)
        if comanda.preticket == None:

            #creo el preticket asociado a la comanda
            #al crear el preticket la fecha y la hora son las del momento en que lo genero
            #de esta menera cuando voy a pretickets tengo arriba los que recien genere
            fecha = datetime.date.today()
            now = datetime.datetime.now()
            hora = datetime.time(now.hour, now.minute, now.second)

            preticket = Preticket.objects.create(fecha=fecha, hora=hora, total=comanda.total(), comanda=comanda)

            #creo los detalles
            for d in comanda.detalles.all():
                detalle_preticket = DetallePreticket.objects.create(cantidad=d.cantidadP, precioXunidad=0,detalleComanda=d)

                if (d.platos) != None:
                    detallePrecio = d.platos.importe()
                    detalle_preticket.platos=d.platos
                else:
                    if (d.bebidas) != None:
                        detallePrecio = d.bebidas.importe()
                        detalle_preticket.bebidas = d.bebidas
                    else:
                        if (d.menuD) != None:
                            detallePrecio = d.menuD.precio
                            detalle_preticket.menuD = d.menuD
                        else:
                            detallePrecio = d.menuE.precio
                            detalle_preticket.menuE = d.menuE

                detalle_preticket.precioXunidad = detallePrecio
                detalle_preticket.save()

                preticket.detalles.add(detalle_preticket)
                preticket.save()
                comanda.preticket = preticket
                comanda.save()

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


    def generar_preticket(self, comanda):
        pass


    def filtrar_secciones(self):
        seccion = SeccionCarta.objects.filter(categoria__exact='B', activo__exact=1)
        return seccion

    def finalizar_comanda(self, comanda):

        comanda.finalizada = True
        comanda.cerrada = True
        fecha = datetime.date.today()
        now = datetime.datetime.now()
        hora = datetime.time(now.hour, now.minute, now.second)
        total = 0

        factura = Factura.objects.create(fecha=fecha, hora=hora, tipo='C', total=total, comanda=comanda)

        for detalles in comanda.detalles.all():
            #total = total + detalles.importe()
            detalleF = detalles.covertir_factura()
            factura.detalle.add(detalleF)


        factura.total = comanda.total()
        factura.save()
        comanda.total = comanda.total()
        comanda.factura = factura
        comanda.save()


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

    tipo_comanda = models.CharField(max_length=1, choices=TIPO_COMANDA)
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    cantidadC = models.DecimalField("CantidadC", max_digits=11, decimal_places=0)
    detalles = models.ManyToManyField(DetalleComanda, related_name="tiene", null=True, blank=True)
    mesas = models.ManyToManyField(Mesa, related_name="ocupa", null=True, blank=True)
    mozo = models.ForeignKey(User, null=True, blank=True)
    vista = models.BooleanField("Vista", default=False)
    finalizada = models.BooleanField("Finalizada", default=False)
    cerrada = models.BooleanField("Cerrada", default=False)
    #si es un pedido
    factura = models.ForeignKey("Factura", null=True, blank=True,related_name="comanda_factura")
    #si es una comanda
    preticket = models.ForeignKey("Preticket", null=True, blank=True,related_name="comanda_preticket")
    total = models.DecimalField("CantidadC", max_digits=11, decimal_places=2, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.estrategia = EstrategiaServicio.obtenerEstrategia(self)

        if type(self.estrategia) is EstrategiaComanda:
            self.tipo_comanda = "C";
        else:
            self.tipo_comanda = "P"


    def total(self):
        aux = 0
        for c in self.detalles.all():
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


    def cerrar(self):
        self.estrategia.cerrar_comanda(self)


class DetallePreticket(models.Model):
    cantidad = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    precioXunidad = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    platos = models.ForeignKey(Plato, null=True, blank=True)
    bebidas = models.ForeignKey(Bebida, null=True, blank=True)
    menuD = models.ForeignKey(DelDia, null=True, blank=True)
    menuE = models.ForeignKey(Ejecutivo, null=True, blank=True)
    detalleComanda = models.ForeignKey(DetalleComanda)

    def importe(self):
        return self.cantidad*self.precioXunidad

class Preticket(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    total = models.DecimalField("Total", max_digits=11, decimal_places=2)
    detalles = models.ManyToManyField(DetallePreticket, related_name="compuesto", null=True, blank=True)
    comanda = models.ForeignKey(Comanda,related_name="preticket_comanda")
    factura = models.ForeignKey("Factura", null=True, blank=True,related_name="preticket_factura")

    def generar_factura(self):

        fecha = datetime.date.today()
        now = datetime.datetime.now()
        hora = datetime.time(now.hour, now.minute, now.second)
        total = 0

        factura_nueva = Factura.objects.create(fecha=fecha, hora=hora, tipo='C', total=total, preticket=self)
        for d in self.detalles.all():

            total = total + d.importe()
            detalleFactura = DetalleFactura.objects.create(cantidad=d.cantidad,precioXunidad=d.precioXunidad,detallePreticket=d)
            factura_nueva.detalle.add(detalleFactura)

        factura_nueva.total = total
        factura_nueva.save()

        self.factura = factura_nueva



class DetallePago(models.Model):
    importe = models.DecimalField("importe", max_digits=11, decimal_places=2)
    tipoPago = models.CharField("Tipo", choices=TIPO_PAGO, max_length=2)


class Pago(models.Model):
    fecha = models.DateField("Fecha")
    total = models.DecimalField("Total_pago", max_digits=11, decimal_places=2)
    detalles = models.ManyToManyField(DetallePago, related_name="detalle_pago", null=True, blank=True)



class DetalleFactura(models.Model):
    cantidad = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    precioXunidad = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    #solo en los pedidos
    detalleComanda = models.ForeignKey(DetalleComanda, null=True, blank=True)
    #solo en las comandas
    detallePreticket = models.ForeignKey(DetallePreticket, null=True, blank=True)


class Factura(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    tipo = models.CharField("Tipo", choices=TIPO, max_length=1)
    total = models.DecimalField("Total", max_digits=11, decimal_places=2)
    detalle = models.ManyToManyField(DetalleFactura, related_name="contiene", null=True, blank=True)
    #si es pedido
    comanda = models.ForeignKey(Comanda, null=True, blank=True,related_name="factura_comanda")
    #si es comanda
    preticket = models.ForeignKey(Preticket, null=True, blank=True,related_name="factura_preticket")
    pago = models.ForeignKey(Pago, null=True, blank=True)