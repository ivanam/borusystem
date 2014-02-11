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

        #TODO nombre prod
        detalle.nombre = producto.nombre
        detalle.save()
        comanda.detalles.add(detalle)
        comanda.save()

    def facturar(self, comanda):
        pass

    def filtrar_secciones(self):
        seccion = SeccionCarta.objects.filter(activo__exact=1).order_by("-categoria","nombre")
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

            preticket = Preticket.objects.create(fecha=fecha, hora=hora, total_preticket=comanda.total(), comanda=comanda)

            #creo los detalles
            for d in comanda.detalles.all():
                detalle_preticket = DetallePreticket.objects.create(preticket=preticket, cantidad=d.cantidadP, precioXunidad=d.precioXunidad,descuento=d.descuento,detalleComanda=d)

                if (d.platos) != None:
                    detalle_preticket.platos=d.platos
                else:
                    if (d.bebidas) != None:
                        detalle_preticket.bebidas = d.bebidas
                    else:
                        if (d.menuD) != None:
                            detalle_preticket.menuD = d.menuD
                        else:
                            detalle_preticket.menuE = d.menuE


                #TODO nombre prod
                detalle_preticket.nombre = d.nombre
                detalle_preticket.save()

                preticket.detalles.add(detalle_preticket)
                preticket.save()
                comanda.preticket = preticket
                comanda.save()

class EstrategiaPedido(EstrategiaServicio):

    def cargarProductos(self, comanda, producto, cantidad):

        if type(producto) is Bebida:

            detalle = DetalleComanda.objects.create(cantidadP=cantidad)
            detalle.bebidas = producto
            #TODO nombre prod
            detalle.nombre = producto.nombre
            detalle.save()
            comanda.detalles.add(detalle)
            comanda.save()

        else:
            print("El producto no se puede cargar")




    def facturar(self, comanda):
        pass


    def generar_preticket(self, comanda):
        pass


    def filtrar_secciones(self):
        seccion = SeccionCarta.objects.filter(categoria__exact='B', activo__exact=1).order_by("-categoria","nombre")
        return seccion

    def finalizar_comanda(self, comanda):

        comanda.finalizada = True
        comanda.cerrada = True
        fecha = datetime.date.today()
        now = datetime.datetime.now()
        hora = datetime.time(now.hour, now.minute, now.second)
        total = 0

        factura = Factura.objects.create(fecha=fecha, hora=hora, tipo='C', total_factura=total, comanda=comanda)

        for detalles in comanda.detalles.all():

            detalleF = detalles.covertir_factura()
            factura.detalle.add(detalleF)


        factura.total_factura = comanda.total()
        factura.save()
        comanda.total = comanda.total()
        comanda.factura = factura
        comanda.save()


ESTRATEGIAS.append(EstrategiaPedido("Pub", datetime.time(0, 0, 0), datetime.time(6, 59, 59)))
ESTRATEGIAS.append(EstrategiaComanda("Resto", datetime.time(7, 0, 0), datetime.time(23, 59, 59)))


class DetalleComanda(models.Model):
    nombre = models.CharField("Nombre",max_length=50,null=False,blank=False)
    cantidadP = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    entregado = models.BooleanField("Entregado", default=False)
    platos = models.ForeignKey(Plato, null=True, blank=True)
    bebidas = models.ForeignKey(Bebida, null=True, blank=True)
    menuD = models.ForeignKey(DelDia, null=True, blank=True)
    menuE = models.ForeignKey(Ejecutivo, null=True, blank=True)
    #TODO agregados ya con descuento el precio
    precioXunidad=models.DecimalField("PrecioXunidad_comanda", max_digits=11, decimal_places=2)
    #el descuent solo a modo informativo
    descuento=models.DecimalField("Descuento_comanda", max_digits=3, decimal_places=0, null=True, blank=True)

    def importe(self):
        return self.precioXunidad * self.cantidadP

    def covertir_factura(self):
        detalle = DetalleFactura.objects.create(cantidad=self.cantidadP, precioXunidad=self.precioXunidad,descuento=self.descuento, detalleComanda=self)
        #TODO nombre prod
        detalle.nombre = self.nombre
        detalle.save()
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
    total = models.DecimalField("Total_comanda", max_digits=11, decimal_places=2, null=True, blank=True)

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
    nombre = models.CharField("Nombre", max_length=50, null=False, blank=False)
    cantidad = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    precioXunidad = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    platos = models.ForeignKey(Plato, null=True, blank=True)
    bebidas = models.ForeignKey(Bebida, null=True, blank=True)
    menuD = models.ForeignKey(DelDia, null=True, blank=True)
    menuE = models.ForeignKey(Ejecutivo, null=True, blank=True)
    detalleComanda = models.ForeignKey(DetalleComanda, null=True, blank=True)
    descuento=models.DecimalField("Descuento_preticket", max_digits=3, decimal_places=0, null=True, blank=True)
    preticket = models.ForeignKey("Preticket", null=False, blank=False)

    def importe(self):
        return self.cantidad*self.precioXunidad


class Preticket(models.Model):

    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    total_preticket = models.DecimalField("Total_preticket", max_digits=11, decimal_places=2, null=True, blank=True)
    detalles = models.ManyToManyField(DetallePreticket, related_name="compuesto", null=True, blank=True)
    comanda = models.ForeignKey(Comanda,related_name="preticket_comanda")
    factura = models.ForeignKey("Factura", null=True, blank=True,related_name="preticket_factura")

    def total(self):
        aux = 0
        for c in self.detalles.all():
            aux = aux + c.importe()

        return aux

    def limpiarDetalles(self):
        d = DetallePreticket.objects.filter(preticket = self).delete()

    def agregarDetalle(self, producto, cantidad):
        #creo el nuevo detalle
        detalle_preticket = DetallePreticket.objects.create(preticket=self, cantidad=cantidad, precioXunidad=producto.importe())
        #leagrego el nombre del producto
        detalle_preticket.nombre = producto.nombre
        #le agrego el producto
        if type(producto) is Plato:
            detalle_preticket.platos = producto
            detalle_preticket.descuento = producto.descuento
        else:
            if type(producto) is Bebida:
                detalle_preticket.bebidas = producto
                detalle_preticket.descuento = producto.descuento
            else:
                if type(producto) is DelDia:
                    detalle_preticket.menuD = producto
                else:
                    detalle_preticket.menuE = producto
        #guardo el detalle con los nuevos datos
        detalle_preticket.save()
        #agrego el detalle a la lista de detelles del preticket
        self.detalles.add(detalle_preticket)
        #salvo el preticket
        self.save()
        #actualizo total del preticket
        self.total_preticket = self.total()
        self.save()


    def generar_factura(self):

        fecha = datetime.date.today()
        now = datetime.datetime.now()
        hora = datetime.time(now.hour, now.minute, now.second)
        total = 0

        factura_nueva = Factura.objects.create(fecha=fecha, hora=hora, tipo='C', total_factura=total, preticket=self)

        for d in self.detalles.all():

            total = total + d.importe()
            detalleFactura = DetalleFactura.objects.create(nombre=d.nombre,cantidad=d.cantidad,precioXunidad=d.precioXunidad,descuento=d.descuento,detallePreticket=d)
            factura_nueva.detalle.add(detalleFactura)

        factura_nueva.total_factura = total
        factura_nueva.save()

        self.factura = factura_nueva
        self.save()


class DetallePago(models.Model):
    importe = models.DecimalField("importe", max_digits=11, decimal_places=2)
    tipoPago = models.CharField("Tipo", choices=TIPO_PAGO, max_length=2,default="E")


class Pago(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    total = models.DecimalField("Total_pago", max_digits=11, decimal_places=2)
    detalles = models.ForeignKey(DetallePago, related_name="detalle_pago", null=True, blank=True)



class DetalleFactura(models.Model):
    nombre = models.CharField("Nombre", max_length=50, null=False, blank=False)
    cantidad = models.DecimalField("CantidadP", max_digits=11, decimal_places=0)
    precioXunidad = models.DecimalField("Precio", max_digits=11, decimal_places=2)
    #solo en los pedidos
    detalleComanda = models.ForeignKey(DetalleComanda, null=True, blank=True)
    #solo en las comandas
    detallePreticket = models.ForeignKey(DetallePreticket, null=True, blank=True)
    descuento=models.DecimalField("Descuento_factura", max_digits=3, decimal_places=0, null=True, blank=True)

    def importe(self):
        return self.cantidad * self.precioXunidad


class Factura(models.Model):
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora")
    tipo = models.CharField("Tipo", choices=TIPO, max_length=1)
    total_factura = models.DecimalField("Total_factura", max_digits=11, decimal_places=2, null=True, blank=True)
    detalle = models.ManyToManyField(DetalleFactura, related_name="contiene", null=True, blank=True)
    #si es pedido
    comanda = models.ForeignKey(Comanda, null=True, blank=True,related_name="factura_comanda")
    #si es comanda
    preticket = models.ForeignKey(Preticket, null=True, blank=True,related_name="factura_preticket")
    pago = models.ForeignKey(Pago, null=True, blank=True)


    def total(self):
        aux = 0
        for c in self.detalle.all():
            aux = aux + c.importe()

    def realizar_pago(self):

        fecha = datetime.date.today()
        now = datetime.datetime.now()
        hora = datetime.time(now.hour, now.minute, now.second)

        pago_nuevo = Pago.objects.create(fecha=fecha,hora=hora,total=self.total_factura)
        detalle_pago_nuevo = DetallePago.objects.create(importe=self.total_factura,tipoPago="E")
        detalle_pago_nuevo.save()
        pago_nuevo.detalle = detalle_pago_nuevo;
        pago_nuevo.save()

        listado_de_mesas=[]
        if self.comanda != None:
            listado_de_mesas = self.comanda.mesas.all()
        else:
            listado_de_mesas = self.preticket.comanda.mesas.all()

        for m in listado_de_mesas:
            m.desocupar()

        self.pago=pago_nuevo
        self.save()