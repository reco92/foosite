from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Cliente(models.Model):
	usuario = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	nombre = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	email = models.EmailField(max_length=75)
	status = models.BooleanField(default=True)
	
	def __unicode__(self):
		nombrecompleto = self.nombre + ' ' + self.apellidos
		return nombrecompleto
	
class Restaurante(models.Model):
	usuario = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	nombre = models.CharField(max_length=200)
	email = models.EmailField(max_length=75)
	telefono = models.CharField(max_length=20)
	descripcion = models.CharField(max_length=350)
	reservaciones = models.IntegerField()
	
	def __unicode__(self):
		return self.nombre
		
class Registro_reservacion(models.Model):
	id_restaurante = models.ForeignKey(Restaurante)
	#id_cliente = models.ForeignKey(Cliente)
	id_cliente = models.ForeignKey(User)
	hora = models.CharField(max_length=20)
	dia = models.CharField(max_length=20)
	status = models.CharField(max_length=2) # p en proceso, n esta negado, a aceptado
	
	def __unicode__(self):
		return str(self.id_restaurante) + ' ' + str(self.id_cliente) + ' '+ self.hora + ' '+ self.dia

class Platillo(models.Model):
	id_restaurante = models.ForeignKey(Restaurante)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=200)
	costo = models.CharField(max_length=10)
	status = models.BooleanField(default=True) # True en venta, False no esta en venta
	def __unicode__(self):
		return str(self.id_restaurante) + ' ' + str(self.nombre)

class Registro_pedido(models.Model):
	#id_cliente = models.ForeignKey(Cliente)
	id_cliente = models.ForeignKey(User)
	id_platillo = models.ForeignKey(Platillo)
	status = models.CharField(max_length=2) # p en proceso, n esta negado, a aceptado
	def __unicode__(self):
		return str(self.id_cliente) + ' ' + str(self.id_platillo)
#staff
