from datetime import datetime
from datetime import time


class Producto(object):
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


class Bebida(Producto):
    pass


class Plato(Producto):
    pass


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

    def consumir(self, producto, comanda):
        pass

    def facturar(self, comanda):
        pass


class EstrategiaPub(EstrategiaServicio):
    def consumir(self, producto, comanda):
        if not isinstance(producto, Plato):
            comanda.productos.append(producto)

    def facturar(self, comanda):
        total = 0
        for p in comanda.productos:
            total += p.precio
        return total


class EstrategiaResto(EstrategiaServicio):
    def consumir(self, producto, comanda):
        comanda.productos.append(producto)

    def facturar(self, comanda):
        total = 0
        for p in comanda.productos:
            total += p.precio
        return total


class EstrategiaPizza(EstrategiaServicio):
    def consumir(self, producto, comanda):
        if producto.nombre == "Pizza" or isinstance(producto, Bebida):
            comanda.productos.append(producto)


class EstrategiaClientesVip(EstrategiaServicio):
    def __init__(self):
        self.clientes = []


ESTRATEGIAS.append(EstrategiaPub("Pub", time(0), time(6, 59)))
ESTRATEGIAS.append(EstrategiaResto("Resto", time(9), time(23, 59)))
ESTRATEGIAS.append(EstrategiaPizza("Pizza", time(7), time(8, 59)))


class Comanda(object):
    def __init__(self, hora, cliente):
        self.productos = []
        self.hora = hora #datetime.now().time()
        self.estrategia = EstrategiaServicio.obtenerEstrategia(self)
        self.cliente = cliente

    def consumir(self, producto):
        self.estrategia.consumir(producto, self)

    def cerrar(self):
        total = self.estrategia.facturar(self)
        print(total)


if __name__ == '__main__':
    comanda1 = Comanda(time(8), "Pepe")
    comanda2 = Comanda(time(3), "Otro")
    comanda1.consumir(Bebida("Cerveza", 15))
    comanda1.consumir(Plato("Pizza", 86))
    comanda2.consumir(Bebida("Cerveza", 15))
    comanda2.consumir(Plato("Fideos", 86))
    comanda1.cerrar()
    comanda2.cerrar()
