# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import *

class Personal(User):

    TURNOS_MOZOS = (("Noche", "Noche"), ("Tarde", "Tarde"), ("Maniana", "Maniana"),)

    DNI_TIPOS = (("DNI","Documento Nacional de Identidad"), ("LC","Libreta Civica"), ("LE","Libreta de Errolamiento"),)

    User.add_to_class('direccion', models.CharField("Direccion", max_length=50, null=True, blank=True))
    User.add_to_class('telefono', models.CharField("Telefono", max_length=20, null=True, blank=True))
    User.add_to_class('tipoDoc', models.CharField("Tipo Documento", max_length=3, choices=DNI_TIPOS, null=True, blank=True,default="DNI"))
    User.add_to_class('numeroDoc', models.CharField("Nº Documento", max_length=8, null=True, blank=True))
    User.add_to_class('turno', models.CharField("Turno", max_length=10, choices=TURNOS_MOZOS, null=True, blank=True,default="Noche"))

    def __str__(self):
        return self.first_name+" "+self.last_name


    class Meta:
        ordering =["first_name"]