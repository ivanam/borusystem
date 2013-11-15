from django.db import models
from gestiones.Producto.producto.models import Plato, Bebida, DelDia, Ejecutivo

CATEGORIA = (
    ('P', 'Plato'),
    ('B', 'Bebida'),
    ('D', 'Menu del Dia'),
    ('E', 'Menu Ejecutivo'),
)

IMAGENES = (
    ('default.png', 'Default'),
    ('bebidas.png', 'Bebidas'),
    ('bebidascalientes.png', 'Bebidas Caliente'),
    ('cafes.png', 'Cafes'),
    ('cervezas.png', 'Cervezas'),
    ('copas.png', 'Copas'),
    ('gaseosas.png', 'Gaseosas'),
    ('jugos.png', 'Jugos'),
    ('pescados.png', 'Pescados'),
    ('pizzas.png', 'Pizzas'),
    ('platos.png', 'Platos'),
    ('platoscalientes.png', 'Platos Calientes'),
    ('postres.png', 'Postres'),
    ('preparados.png', 'Preparados'),
    ('tortas.png', 'Tortas'),
    ('vinos.png', 'Vinos'),
)


class SeccionCarta(models.Model):
    nombre = models.CharField('Nombre', max_length=30, blank=True)
    categoria = models.CharField('Categoria', max_length=1, choices=CATEGORIA)
    activo = models.BooleanField('Activo', default=True)
    cartavigente = models.ForeignKey('Carta')
    platoss = models.ManyToManyField(Plato, null=True, related_name='contiene1')
    bebidas = models.ManyToManyField(Bebida, null=True, related_name='contiene2')
    menuesD = models.ManyToManyField(DelDia, null=True, related_name='contiene3')
    menuesE = models.ManyToManyField(Ejecutivo, null=True, related_name='contiene3')
    imagen = models.CharField("Imagen",max_length=35, choices=IMAGENES, default="default.png", null=False,blank=False)
    def __str__(self):
        return self.nombre

    def dame_productos(self):
        if self.categoria == 'P':
            return Plato.objects.filter(seccion_id__exact=self.id)
        else:
            if self.categoria == 'B':
                return Bebida.objects.filter(seccion_id__exact=self.id)
            else:
                if self.categoria == 'D':
                    return DelDia.objects.filter(seccion_id__exact=self.id)
                else:
                    return Ejecutivo.objects.filter(seccion_id__exact=self.id)

class Carta(models.Model):
    nombre = models.CharField('Nombre', max_length=30)
    vigente = models.BooleanField('Vigente')
    fecha = models.DateField('Fecha',blank=True)
    secciones = models.ManyToManyField('SeccionCarta', null=True,related_name='compuesta')






